###Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

#####2021-03-06
Changed
- Overhaul of project structure and direction. I'd rather focus on getting a distributed solution working locally,
then move it to the cloud
- I'm also in the process of refactoring the code to adhere more closely to OOP.
- See [board](https://github.com/aroussel-data/un_data_aggregator/projects/2) for more details.

#####2020-04-29
Added
- Use of temp table for writing updated data files to table as data_id (which I assumed was unique
  to a particular event record, can in fact change but still reference the same event, which IMO would introduce
  unnecessary duplicates.

Changed
- Specify *event_id_cnty* as the primary key and use INSERT IGNORE to write only new records
 to the table, preserving the state of existing records in the table. This may change in the future.

#####2020-04-28
Fixed
- Upgraded Lambda runtime memory to process larger files (tested up to 33MB).

#####2020-04-27
Changed
- Pipeline from EC2->S3->RDS has been automated
- Lambda retries a failed attempt twice by default, so have set retries=0 and instead routes failures to an SQS queue
  where they will be picked up later.
- Failures are due to larger files exceeding the 128MB memory on a Lambda invocation. Will test with more memory.


#####2020-04-25
Added
- Added VPC endpoint to S3 in order for Lambda function to access S3 files, as Lambda gets launched in its own VPC. After some struggle, realised that if my Lambda function is set to use the VPC that RDS is in, I need to create a
  VPC endpoint for S3, otherwise Lambda won't be able to access it...

#####2020-04-23
Added
- Set up a listener on S3 to trigger Lambda function when a csv is uploaded to S3. 

Deprecated
- If all files are uploaded to S3 at once, Lambda's invocations exceed the max connection pools for the RDS instance. 
- For now, this works because files are uploaded every second or so, however, I'd like to add the S3 upload events to 
their own SQS queue so as not to lose any uploads.

#####2020-04-22
Deprecated
- Initial attempt using DynamoDB was quickly exceeding the provisioned write capacity units
  and was not going to be sustainable, especially doing batch writes. 
- Need to redo file upload to include the column headers otherwise will be a pain writing to db.

Added
- Writing data to RDS using SQL Alchemy.




