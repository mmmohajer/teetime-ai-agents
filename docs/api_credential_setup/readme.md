# 🔐 API & Cloud Service Credentials Setup Guide

This project integrates with multiple third-party services (Google Cloud, OpenAI, AWS, Azure, SendGrid, etc.).  
This document explains how to create accounts, obtain API credentials, and configure them via environment variables.

---

## Table of Contents

- [1. Google Cloud Platform (GCP)](#1-google-cloud-platform-gcp)
  - [1.1 Create an Account](#11-create-an-account)
  - [1.2 Enable Required APIs](#12-enable-required-apis)
  - [1.3 Create a Service Account](#13-create-a-service-account)
  - [1.4 Store Credentials](#14-store-credentials)
- [2. OpenAI](#2-openai)
  - [2.1 Create an Account](#21-create-an-account)
  - [2.2 Generate API Key](#22-generate-api-key)
  - [2.3 Set Environment Variable](#23-set-environment-variable)
- [3. AWS (Amazon Web Services)](#3-aws-amazon-web-services)
  - [3.1 Create an Account](#31-create-an-account)
  - [3.2 Create IAM User](#32-create-iam-user)
  - [3.3 Set Environment Variables](#33-set-environment-variables)
- [4. Azure Cognitive Services (Speech)](#4-azure-cognitive-services-speech)
  - [4.1 Create an Account](#41-create-an-account)
  - [4.2 Create a Speech Resource](#42-create-a-speech-resource)
  - [4.3 Obtain Keys & Region](#43-obtain-keys--region)
  - [4.4 Set Environment Variables](#44-set-environment-variables)
- [5. SendGrid (Transactional Emails)](#5-sendgrid-transactional-emails)
  - [5.1 Create an Account](#51-create-an-account)
  - [5.2 Create API Key](#52-create-api-key)
  - [5.3 Set Environment Variable](#53-set-environment-variable)
- [✅ Final Notes](#-final-notes)

---

## 1. Google Cloud Platform (GCP)

### 1.1 Create an Account

- Sign up: [https://cloud.google.com/](https://cloud.google.com/)
- Activate a project in the **Google Cloud Console**.

### 1.2 Enable Required APIs

Enable the following APIs in your project:

- **Document AI**
- **Cloud Vision API**
- **Text-to-Speech API**
- **Speech-to-Text API**

### 1.3 Create a Service Account

1. Go to: [Service Accounts Console](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Create a new service account.
3. Assign roles such as:
   - `Document AI Editor`
   - `Cloud Vision API User`
   - `Text-to-Speech Editor`
   - `Speech-to-Text Editor`
4. Download the JSON key file.

### 1.4 Store Credentials

- Save the JSON file securely.
- Set environment variable in `.env`:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
  GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID=<YOUR_PROJECT_ID>
  GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID=<PROCESSOR_ID>
  GOOGLE_API_KEY=<API_KEY>
  ```

📚 Docs: [https://cloud.google.com/docs/authentication](https://cloud.google.com/docs/authentication)

---

## 2. OpenAI

### 2.1 Create an Account

- Sign up: [https://platform.openai.com/](https://platform.openai.com/)

### 2.2 Generate API Key

- Go to: [API Keys Page](https://platform.openai.com/account/api-keys)
- Click **Create new secret key**.

### 2.3 Set Environment Variable

```
OPEN_AI_SECRET_KEY=sk-xxxxxx
```

📚 Docs: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)

---

## 3. AWS (Amazon Web Services)

### 3.1 Create an Account

- Sign up: [https://aws.amazon.com/](https://aws.amazon.com/)

### 3.2 Create IAM User

1. Go to [IAM Console](https://console.aws.amazon.com/iam/).
2. Create a new user with **Programmatic access**.
3. Attach policies (e.g., `AmazonS3FullAccess` for storage).
4. Download **Access Key ID** and **Secret Access Key**.

### 3.3 Set Environment Variables

```
AWS_ACCESS_KEY_ID=<ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<SECRET_ACCESS_KEY>
AWS_DEFAULT_REGION=us-east-1
```

📚 Docs: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)

---

## 4. Azure Cognitive Services (Speech)

### 4.1 Create an Account

- Sign up: [https://azure.microsoft.com/](https://azure.microsoft.com/)

### 4.2 Create a Speech Resource

1. Go to [Azure Portal](https://portal.azure.com/).
2. Create a new **Cognitive Services – Speech** resource.
3. After deployment, open the resource.

### 4.3 Obtain Keys & Region

- Under **Keys and Endpoint**, copy:
  - `Key1` and `Key2`
  - Service Region (e.g., `eastus`)

### 4.4 Set Environment Variables

```
AZURE_COGNITIVE_SERVICES_KEY_1=<KEY1>
AZURE_COGNITIVE_SERVICES_KEY_2=<KEY2>
AZURE_COGNITIVE_SERVICES_REGION=<REGION>
```

📚 Docs: [https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/)

---

## 5. SendGrid (Transactional Emails)

### 5.1 Create an Account

- Sign up: [https://sendgrid.com/](https://sendgrid.com/)

### 5.2 Create API Key

1. Go to: [API Keys](https://app.sendgrid.com/settings/api_keys).
2. Click **Create API Key**.
3. Give it **Full Access** or **Restricted Access** depending on your needs.

### 5.3 Set Environment Variable

```
SENDGRID_API_KEY=SG.xxxxx
```

📚 Docs: [https://docs.sendgrid.com/](https://docs.sendgrid.com/)

---

## ✅ Final Notes

- Always keep keys **secret** (never commit them to Git).
- Rotate keys regularly for security.
- Use `.env` files with `python-dotenv` in Django.
- For production, inject secrets via Docker secrets, Kubernetes secrets, or environment variables in your CI/CD pipeline.
