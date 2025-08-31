import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';



const options = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'My Express API',
            version: '1.0.0',
            description: 'A simple CRUD API with Express and Swagger',
        },
        servers: [
            {
                url: 'http://ec2-13-126-1-128.ap-south-1.compute.amazonaws.com:8000'
            },
        ],
        components: {
            securitySchemes: {
                bearerAuth: {
                    type: 'http',
                    scheme: 'bearer',
                    bearerFormat: 'JWT',
                },
            },
        },
        security: [
            {
                bearerAuth: [],
            },
        ],
    },
    apis: [
        './myapp/swagger_docs/*.js',
    ],
};

const swaggerSpec = swaggerJsdoc(options);

export { swaggerUi, swaggerSpec };