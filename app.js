import express from 'express';
import cors from 'cors';
import { z } from 'zod';
import { logger, SUPPORTED_SITES } from './config.js';
import { EmailProcessor } from './email-utils/processor.js';
import { ScraperFactory } from './factory/scraper-factory.js';
import { isValidEmail } from './email-utils/validator.js';
import { v4 as uuidv4 } from 'uuid';

const app = express();
app.use(express.json());
app.use(cors({
    origin: "*", // In production, replace with specific frontend URL
    credentials: true,
    methods: ["*"],
    allowedHeaders: ["*"]
}));

// Initialize processor
const emailProcessor = new EmailProcessor();
const scraperFactory = ScraperFactory;

// Store task results (in production, use Redis or database)
const taskResults = {};

// Request validation schemas
const subscribeRequestSchema = z.object({
    url: z.string().min(1, "URL must be a non-empty string").refine((url) => {
        return scraperFactory.isSupportedUrl(url);
    }, (url) => ({
        message: `Unsupported website URL. Supported sites: ${scraperFactory.getSupportedSitesList()}`
    })),
    emails: z.array(z.string().email()).min(1, "At least one email address is required"),
    headless: z.boolean().default(true)
});

// Background task to process emails
async function processSubscriptionTask(taskId, url, emails, headless) {
    try {
        const results = await emailProcessor.processEmails(url, emails, headless);
        taskResults[taskId] = {
            status: "completed",
            ...results,
            url: url
        };
    } catch (error) {
        taskResults[taskId] = {
            status: "failed",
            total: emails.length,
            success: 0,
            failed: emails.length,
            errors: [error.message],
            url: url
        };
    }
}

// API Endpoints
app.get('/', (req, res) => {
    res.json({
        status: "healthy",
        message: "Newsletter Subscription API is running"
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: "healthy",
        message: "API is operational"
    });
});

app.get('/sites', (req, res) => {
    const sitesList = Object.keys(SUPPORTED_SITES);
    res.json({
        supported_sites: sitesList,
        site_details: SUPPORTED_SITES
    });
});

app.post('/subscribe', async (req, res) => {
    try {
        // Validate request
        const validationResult = subscribeRequestSchema.safeParse(req.body);
        if (!validationResult.success) {
            return res.status(400).json({
                error: "Validation failed",
                details: validationResult.error.errors
            });
        }

        const { url, emails, headless } = validationResult.data;
        
        // Generate task ID
        const taskId = uuidv4();
        
        // Initialize task status
        taskResults[taskId] = {
            status: "processing",
            total: emails.length,
            success: 0,
            failed: 0,
            errors: [],
            url: url
        };
        
        // Start background processing (non-blocking)
        processSubscriptionTask(taskId, url, emails, headless).catch(error => {
            logger.error(`Background task error for ${taskId}: ${error.message}`);
        });
        
        logger.info(`Created subscription task ${taskId} for ${emails.length} email(s) at ${url}`);
        
        // Return immediately with task ID
        res.status(202).json({
            task_id: taskId,
            message: `Subscription task created for ${emails.length} email(s)`,
            status: "processing",
            url: url,
            total_emails: emails.length
        });
    } catch (error) {
        logger.error(`Error in /subscribe endpoint: ${error.message}`);
        res.status(500).json({
            error: "Internal server error",
            message: error.message
        });
    }
});

app.get('/subscribe/:taskId', (req, res) => {
    const { taskId } = req.params;
    
    if (!taskResults[taskId]) {
        return res.status(404).json({
            error: "Task not found",
            message: `Task ${taskId} not found`
        });
    }
    
    const result = taskResults[taskId];
    res.json({
        task_id: taskId,
        status: result.status,
        total: result.total,
        success: result.success,
        failed: result.failed,
        errors: result.errors || [],
        url: result.url || ""
    });
});

const PORT = process.env.PORT || 8000;

app.listen(PORT, '0.0.0.0', () => {
    logger.info(`Server running on port ${PORT}`);
});

export default app;

