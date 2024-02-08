'''
import requests
from PIL import Image
from io import BytesIO

def fetch_logo_image_url(company_name):
    api_url = f'https://api.api-ninjas.com/v1/logo?name={company_name}'
    response = requests.get(api_url, headers={'X-Api-Key': 'dh7gTBxCZW4BcUhEiFzceA==M3DioFtZJ5HDx9w4'})

    if response.status_code == 200:
        
        data = response.json()
        
        if data and 'image' in data[0]:
            return data[0]['image']
        else:
            return "No image found."
    else:
        return "Error:", response.status_code, response.text


company_name = 'Apple'
image_url = fetch_logo_image_url(company_name)
print(image_url)


def check_image_size_and_format(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        size = img.size  # Size in pixels (width, height)
        format = img.format  # Format like 'JPEG', 'PNG', etc.
        return size, format
    else:
        return None, None

# Example usage
url = "https://api-ninjas-data.s3.us-west-2.amazonaws.com/logos/l476432a3e85a0aa21c23f5abd2975a89b6820d63.png"
size, format = check_image_size_and_format(url)
print(f"Size: {size}, Format: {format}")

def resize_image(url, max_size=(400, 400)):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size, Image.ANTIALIAS)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    else:
        return None

# Example usage
url = "https://api-ninjas-data.s3.us-west-2.amazonaws.com/logos/l476432a3e85a0aa21c23f5abd2975a89b6820d63.png"
resized_image_buffer = resize_image(url)
'''



'''
def resize_and_show_image(url, max_size=(400, 400)):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        original_size = img.size  # Store the original image size
        img.thumbnail(max_size)  

        # Display the reduced image using matplotlib
        plt.imshow(img)
        plt.title("")
        plt.axis('off')
        plt.show()

        return original_size, img.size  # Return both original and reduced sizes
    else:
        return None, None

def fetch_logo_image_url(symbol):
    api_url_name = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
    api_url_ticker = f'https://api.api-ninjas.com/v1/logo?name={symbol}&ticker=true'
    
    try:
        # Try fetching by company name first
        response = requests.get(api_url_name, headers={'X-Api-Key': 'dh7gTBxCZW4BcUhEiFzceA==M3DioFtZJ5HDx9w4'})
        if response.status_code == 200:
            data = response.json()
            if data and 'image' in data[0]:
                return data[0]['image']
        
        # If the company name query didn't return an image, try fetching by ticker
        response_ticker = requests.get(api_url_ticker, headers={'X-Api-Key': 'dh7gTBxCZW4BcUhEiFzceA==M3DioFtZJ5HDx9w4'})
        if response_ticker.status_code == 200:
            data_ticker = response_ticker.json()
            if data_ticker and 'image' in data_ticker[0]:
                return data_ticker[0]['image']

        # If both queries failed, print an error message
        print(f"No image found for symbol {symbol}.")
        return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None

# Function to fetch and display logo by symbol or name
def fetch_and_display_logo(symbol):
    # Get the company name from the ticker symbol
    company_name = get_company_name_from_ticker(symbol)

    if company_name:
        # Fetch and resize the logo using the company name
        logo_url = fetch_logo_image_url(company_name)
        if logo_url:
            original_size, reduced_size = resize_and_show_image(logo_url)
            if original_size and reduced_size:
                print(f"Original Image Size: {original_size}")
                print(f"Resized Image Size: {reduced_size}")
            else:
                print("Failed to resize and show image.")
        else:
            print(f"No image found for company name {company_name}.")
    else:
        print(f"No company name found for symbol {symbol}.")

# Function to get company name from ticker

def get_company_name_from_ticker(symbol):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your Alpha Vantage API key
    endpoint = f'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': symbol,
        'apikey': api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        if 'bestMatches' in data:
            matches = data['bestMatches']
            if matches:
                # Assuming the first match is the closest match
                full_name = matches[0]['2. name']
                company_name = full_name.split(' ')[0]  # Split by space and take the first part
                return company_name
    except requests.RequestException as e:
        print(f"Error fetching company name: {e}")

    return None


# Example usage:
symbol = 'MSFT'  # Replace with the desired company symbol or name
company_name = get_company_name_from_ticker(symbol)
if company_name:
    print(f"Company Name for {symbol}: {company_name}")
else:
    print(f"No company name found for {symbol}")

fetch_and_display_logo(symbol)
'''
import requests

def fetch_logo_image_url(symbol):
    api_key = 'dh7gTBxCZW4BcUhEiFzceA==M3DioFtZJ5HDx9w4'  # API Ninjas API key
    api_url_name = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
    api_url_ticker = f'https://api.api-ninjas.com/v1/logo?name={symbol}&ticker=true'
    
    try:
        response = requests.get(api_url_name, headers={'X-Api-Key': api_key})
        if response.status_code == 200 and response.json():
            data = response.json()
            if 'image' in data[0]:
                return data[0]['image']

        response_ticker = requests.get(api_url_ticker, headers={'X-Api-Key': api_key})
        if response_ticker.status_code == 200 and response_ticker.json():
            data_ticker = response_ticker.json()
            if 'image' in data_ticker[0]:
                return data_ticker[0]['image']

        print(f"No image found for symbol {symbol}.")
        return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None



def get_company_name_from_ticker(symbol):
    api_key = 'LFCWIHIIY5SRPB7N'  # Alpha Vantage API key
    endpoint = f'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': symbol,
        'apikey': api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200 and response.json():
            data = response.json()
            if 'bestMatches' in data and data['bestMatches']:
                full_name = data['bestMatches'][0]['2. name']
                company_name = full_name.split(' ')[0]  # Split by space and take the first part
                return company_name
        return None
    except requests.RequestException as e:
        print(f"Error fetching company name: {e}")
        return None

# Example usage
symbol = 'GS'
company_name = get_company_name_from_ticker(symbol)
if company_name:
    print(f"Company Name for {symbol}: {company_name}")
    logo_url = fetch_logo_image_url(company_name)  # passing the shortened company name
    if logo_url:
        print(f"Logo URL: {logo_url}")
else:
    print(f"No company name found for {symbol}")
