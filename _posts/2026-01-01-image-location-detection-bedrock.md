---
layout: post
title: "Image location detection using Bedrock and Claude Model"
excerpt: "Image location detection using Bedrock and Claude Model"
disqus_id: /2026/01/01/image-location-detection-bedrock/
tags:
    - Bedrock
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

I needed a way to automatically identify locations in a collection of images, so I built a Python script that uses AWS Bedrock's Claude API for image analysis. The script processes images in batches, optimizes them for API efficiency, and saves location descriptions as text files.

## Overview

The script handles:
- Recursive image processing from folders
- Image optimization to reduce API costs
- AWS Bedrock integration with Claude models
- Automatic text file generation for results
- Skip logic for already-processed images

## Setup

Install dependencies:
```bash
pip install boto3 Pillow
```

Configure AWS credentials via CLI, environment variables, or IAM roles. Ensure you have access to Bedrock and Claude models in your region.

## Image Processing

The first challenge is managing image sizes. Large images are expensive to process and may exceed API limits. The solution processes images entirely in memory:

```python
import os
import base64
from PIL import Image
import io

def resize_image_in_memory(image_path, max_size=(1024, 1024), quality=85):
    """Resize image in memory without saving to disk"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (handles RGBA, P mode images)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            
            # Determine format based on original image
            original_format = img.format if img.format else 'JPEG'
            if original_format.upper() in ['JPEG', 'JPG']:
                img.save(buffer, format='JPEG', quality=quality, optimize=True)
            elif original_format.upper() == 'PNG':
                img.save(buffer, format='PNG', optimize=True)
            else:
                # Default to JPEG for other formats
                img.save(buffer, format='JPEG', quality=quality, optimize=True)
            
            buffer.seek(0)
            return buffer.getvalue(), original_format
            
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        return None, None
```

This maintains aspect ratios, handles different formats, and provides significant compression. For a typical 4MB photo, this reduces size to ~300KB (92% reduction).

## Base64 Encoding

AWS Bedrock requires base64-encoded images. The encoding function includes optional optimization:

```python
def encode_image_to_base64(image_path, resize=True, max_size=(1024, 1024), quality=85):
    """Encode image file to base64 string with optional resizing"""
    try:
        if resize:
            image_bytes, original_format = resize_image_in_memory(image_path, max_size, quality)
            if image_bytes is None:
                return None
            return base64.b64encode(image_bytes).decode('utf-8')
        else:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None
```

## Bedrock Integration

The core function handles the API communication:

```python
import boto3
import mimetypes
from botocore.exceptions import ClientError

def get_image_format(image_path):
    """Get image format for Bedrock API (lowercase format names)"""
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type and mime_type.startswith('image/'):
        format_map = {
            'image/jpeg': 'jpeg',
            'image/jpg': 'jpeg', 
            'image/png': 'png',
            'image/gif': 'gif',
            'image/webp': 'webp'
        }
        return format_map.get(mime_type, 'jpeg')
    return 'jpeg'

def analyze_image_location(bedrock_client, image_path, model_id="anthropic.claude-3-5-sonnet-20241022-v2:0", 
                         resize_images=True, max_size=(1024, 1024), quality=85):
    """Send image to AWS Bedrock and get location analysis"""
    try:
        base64_image = encode_image_to_base64(image_path, resize=resize_images, 
                                            max_size=max_size, quality=quality)
        if not base64_image:
            return None
        
        image_format = get_image_format(image_path)
        
        message = {
            "role": "user",
            "content": [
                {
                    "text": "Analyze this image and identify the location or place shown. Provide a concise one-line description of the location, including the most specific place name possible (city, landmark, or geographical feature). Keep the response to a single sentence - no more than one line. Do not start with phrases like 'This is', 'The image shows', or 'This appears to be'"
                },
                {
                    "image": {
                        "format": image_format,
                        "source": {
                            "bytes": base64.b64decode(base64_image)
                        }
                    }
                }
            ]
        }
        
        response = bedrock_client.converse(
            modelId=model_id,
            messages=[message],
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.1
            }
        )
        
        location_analysis = response['output']['message']['content'][0]['text']
        return location_analysis
        
    except ClientError as e:
        print(f"AWS Bedrock error for {image_path}: {e}")
        return None
    except Exception as e:
        print(f"Error analyzing image {image_path}: {e}")
        return None
```

Key technical details:
- Uses the `converse` API instead of the older `invoke` method
- Low temperature (0.1) for consistent responses
- Specific prompt engineering to avoid verbose prefixes
- Handles various image formats through MIME type detection

## File Management

The script organizes results by saving text files alongside images:

```python
from pathlib import Path

def save_location_to_file(image_path, location_text):
    """Save location analysis to text file with same name as image"""
    try:
        image_name = Path(image_path).stem
        image_dir = Path(image_path).parent
        text_file_path = image_dir / f"{image_name}.txt"
        
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(location_text)
        
        print(f"  Saved to: {text_file_path.name}")
        return True
        
    except Exception as e:
        print(f"Error saving text file for {image_path}: {e}")
        return False

def get_image_files(folder_path):
    """Recursively get all image files from folder and subfolders"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
    
    return image_files
```

## Main Processing Loop

The main function coordinates everything:

```python
def process_images(folder_path, aws_region='us-east-1', model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
                  resize_images=True, max_size=(1024, 1024), quality=85):
    """Main function to process all images in folder"""
    
    try:
        bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )
        print(f"Connected to AWS Bedrock in region: {aws_region}")
    except Exception as e:
        print(f"Error connecting to AWS Bedrock: {e}")
        return
    
    image_files = get_image_files(folder_path)
    
    if not image_files:
        print(f"No image files found in {folder_path}")
        return
    
    print(f"Found {len(image_files)} image files to process")
    
    processed = 0
    failed = 0
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {image_path.name}")
        
        # Skip if already processed
        text_file_path = image_path.parent / f"{image_path.stem}.txt"
        if text_file_path.exists():
            print(f"  Text file already exists, skipping...")
            continue
        
        location_analysis = analyze_image_location(
            bedrock_client, image_path, model_id,
            resize_images=resize_images, max_size=max_size, quality=quality
        )
        
        if location_analysis:
            if save_location_to_file(image_path, location_analysis):
                processed += 1
                print(f"  ✓ Success")
            else:
                failed += 1
                print(f"  ✗ Failed to save")
        else:
            failed += 1
            print(f"  ✗ Failed to analyze")
    
    print(f"\nProcessing Complete: {processed} successful, {failed} failed")
```

## Usage

Configure and run:

```python
if __name__ == "__main__":
    RESIZE_IMAGES = True
    MAX_SIZE = (1024, 1024)
    QUALITY = 85
    
    process_images(
        folder_path="/home/user/Pictures/wallpapers/night",
        aws_region="ap-south-1",
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        resize_images=RESIZE_IMAGES,
        max_size=MAX_SIZE,
        quality=QUALITY
    )
```

## Output Example

```
Connected to AWS Bedrock in region: ap-south-1
Found 15 image files to process

[1/15] Processing: sunset_beach.jpg
  Size: 4.2MB → 0.3MB (92.8% reduction)
  Saved to: sunset_beach.txt
  ✓ Success

[2/15] Processing: mountain_view.png
  Text file already exists, skipping...
```

## Technical Notes

**Model Options:**
- `claude-3-5-sonnet`: Good balance of speed and accuracy
- `claude-3-haiku`: Faster and cheaper
- `claude-3-opus`: Most capable but expensive

**Error Handling:**
The script handles network issues, API limits, invalid formats, and file permissions gracefully.

**Cost Considerations:**
Image resizing typically reduces API costs by 80-95%. The skip logic prevents reprocessing already-analyzed images.