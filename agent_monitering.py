import logging
import time
from prometheus_client import start_http_server, Counter, Histogram


# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# prometheus metrics
REQUEST_COUNT = Counter('agent_requests_total', 'Total number of requests to the agent')

ERROR_COUNT = Counter('agent_errors_total', 'Total number of errors encountered by the agent')

RESPONSE_TIME = Histogram('agent_response_time_seconds', 'Time taken for agent to respond')


# agent
class DummyAgent:
    def run(self, query):
        if "error" in query.lower():
            raise ValueError("Simulated agent error!")
        time.sleep(0.5)  # simulate processing time
        return f"Processed : {query}"
    
agent = DummyAgent()

# run agent with logging and metrics
def run_agent_with_monitering(query):
    REQUEST_COUNT.inc()
    logger.info(f"Processing query: {query}")


    start_time = time.time()
    try:
        response = agent.run(query)
        logger.info(f"Agent response: {response}")
    except Exception as e:
        ERROR_COUNT.inc()
        logger.error(f"Agent error: {e}")
        response = None
    finally:
        elapsed_time = time.time() - start_time
        RESPONSE_TIME.observe(elapsed_time)
        logger.info(f"Response time: {elapsed_time:.2f} seconds")
    return response


# start prometheus server
if __name__ == "__main__":
    start_http_server(8000)
    logger.info("Prometheus metrics server started on port 8000")

    # example loop to simulate queries
    queries = [
        "Hello",
        "How are you?",
        "Cause error",
        "Another queries"
    ]
    while True:
        for q in queries:
            run_agent_with_monitering(q)
            time.sleep(1)