<a id="readme-top"></a>

<!-- PROBLEM STATEMENT -->
## Problem Statement

Heygen is a AI powered video creation platform. Video translation is a popular feature that let’s us translate a video from one language to another but with lip sync! 

When you use video translation on Heygen, behind the scenes it is a time consuming process depending on how long the video is and many other factors. 

In this coding exercise you will be writing a client library in your chosen language. You will be simulating the video translation server using a configurable random delay.

**Server: **

You will be writing a server that implements a status API and returns a result that is pending, completed or error. This is just simulating the video translation backend. It will return pending until a configurable time has passed.

GET /status 

Return result with {“result”: “pending” or “error” or “completed”}

**Client Library: **

You are writing a small client library to hit this server endpoint. Imagine you will be giving this library to a third party. They will be using it to get the status of the job. 

In a trivial approach your library might just make a simple http call and wrap the errors and you ask the user of the library to call this repeatedly. If they call it very frequently then it has a cost, if they call it too slowly it might cause unnecessary delays in getting the status.

How can you do better than a trivial approach ? 

Demonstrate customer mindset while writing this library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Flask](https://flask.palletsprojects.com/en/stable/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites

* Python >= 3

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/epchao/heygen-take-home.git
   cd hygen-take-home
   ```
2. Activate the virtual environment
   ```sh
   source .venv/bin/activate
   ```
3. Ensure that the packages are installed
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Use the client library as demonstrated in the ./tests/test_integration.py test suite
   ```python
   status = client.get_status()
   # assert the status as "pending", "completed", or "error"
   ```
2. Run the ./tests/test_integration.py test suite
   ```sh
   python3 -m unittest tests/test_integration.py
   ```

The current test suite checks to see that the status of the job will turn from "pending" to "completed" within 10 seconds (default time delay) of the server starting and will limit test the client to ensure that it can handle a large influx of requests by introducing exponential backoff with the retry requests for an acceptable number of retries.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
