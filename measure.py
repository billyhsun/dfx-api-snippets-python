import argparse
import asyncio

from dfxsnippets.addData import addData
from dfxsnippets.createMeasurement import createMeasurement
from dfxsnippets.subscribeResults import subscribeResults

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DFX API Python snippets example")

    parser.add_argument("studyID", help="StudyID")
    parser.add_argument("token", help="user or device token")
    parser.add_argument("restUrl", help="DFX API REST url")
    parser.add_argument("wsUrl", help="DFX API Websocket url")
    parser.add_argument("payloadDir", help="Directory of payload files")

    args = parser.parse_args()

    studyID = args.studyID
    token = args.token
    rest_url = args.restUrl
    ws_url = args.wsUrl
    input_directory = args.payloadDir

    # Create the async event loop
    loop = asyncio.get_event_loop()

    # Create a measurement object and get a measurement ID
    createmeasurementObj = createMeasurement(studyID, token, rest_url)
    measurementID = createmeasurementObj.create()

    # Create an addData object (which prepares the data need to be sent in the input_directory)
    adddataObj = addData(measurementID, token, rest_url, input_directory)

    # Create a subscribeResults object (which prepares the subscribe request)
    subscriberesultsObj = subscribeResults(measurementID, token, ws_url,
                                           adddataObj.num_chunks)

    # Add tasks to the event loop
    tasks = []
    t = loop.create_task(subscriberesultsObj.subscribe())
    tasks.append(t)

    # Run the event loop until all of it's tasks finish
    loop.run_until_complete(adddataObj.sendAsync())

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()
