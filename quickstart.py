import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1b5WaHVrHdPxm0vyW6DGcScWs8MMa2V42ZWWiTCt3pDc"
SAMPLE_RANGE_NAME = "Action Tracker!A2:J139"


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/Users/vipulkedia/Desktop/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return
      
      
    # owner_tasks = {}
    # for row in values:
    #   try:
    #     if len(row) >= 3:
    #       owner = row[4].strip() if row[4] else None
    #       status = row[7].strip() if row[7] else None
    #       task = row[2].strip() if row[2] else None
    #       print(status)

    #       if status != "Completed":
    #         owner_tasks.setdefault(owner, []).append(task)
    #   except IndexError as e:
    #     continue
    # # print(owner_tasks)
    # return owner_tasks

    owner_tasks = {}

    # Skip the header row and iterate over the rows of data
    for row in values:  # Assuming the first row is the header, adjust if necessary
      # Extract values for 'Task Description', 'Status', and 'Owner' columns
      try:
          task_desc = row[2]  # Assuming 'Task Description' is in the first column (index 0)
          status = row[7] if len(row) > 7 else ''  # Assuming 'Status' is in the second column (index 1)
          owner = row[4] if len(row) > 4 else ''  # Assuming 'Owner' is in the third column (index 2)
      except IndexError:
          continue  # Skip rows that don't have enough columns
      
      # print(status)
      # Check if status is either empty or not 'Completed'
      if status != 'Completed' and (status == '' or not status):
          # Add the task to the owner's list in the dictionary
          if owner not in owner_tasks:
              owner_tasks[owner] = []
          owner_tasks[owner].append(task_desc)
    # print(owner_tasks)
    return owner_tasks
      
      # print(f"{row[0]}, {row[2]}, {row[4]}")
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()