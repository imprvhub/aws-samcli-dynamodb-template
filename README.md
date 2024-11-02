## AWS-SamCLI-DynamoDB-Template

## Overview
This is a serverless solution template built using AWS SAM, Lambda, DynamoDB, and S3. This application is designed to efficiently process and analyze text data in a scalable manner.

## Prerequisites
To set up the application, ensure you have the following installed and configured:

- **AWS CLI**: Command Line Interface for managing AWS services.
- **SAM CLI**: AWS Serverless Application Model Command Line Interface for building and deploying serverless applications.
- **Python 3.12**: The programming language used for the Lambda functions.
- **AWS Account**: An active AWS account is required to deploy the application.

## Installation Steps
Follow these steps to set up the application locally:

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**
   Create a .env file in the root of your project and define the necessary environment variables.
5. **Set Up AWS Credentials**
   ```bash
   aws configure set aws_access_key_id your_access_key
   aws configure set aws_secret_access_key your_secret_key
   aws configure set region your_region
   ```

## Deployment

   ```bash
   sam deploy --guided
   ```
This command will guide you through the deployment process, prompting you for necessary parameters such as stack name, AWS region, and confirmation to create IAM roles.

## Testing
Run the following commands to execute tests:

-Integration Tests:
To run integration tests, execute:

```bash
pytest -v tests/integration/test_lambda_integration.py
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the [MIT](/LICENSE) License.
