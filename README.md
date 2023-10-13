# Python REST Fuzzing
This application is a Web API application written with Python which is used as a fuzzing target to test the implementation of input and business logic validation mechanisms.

This application has 3 types of validation modes, namely no validation, partial validation, and full validation. In partial validation mode, the input validation only checks the data type and does not check data constraints such as minimum and maximum length of the data. For example, if the expected input is integer data type with minimum value of 0 and maximum value of 100, then partial validation mode only checks whether the data type is integer or not and does not check the minimum/maximum size of the data. For full validation mode, validation is also carried out on the minimum/maximum size of the data, in addition to validating the data type.

This application uses the [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) and [Pydantic](https://docs.pydantic.dev/latest/) libraries to validate input payloads.

Currently, the application <b>has no authentication and authorization mechanisms</b> and is only used for research and testing purposes.

## Functionality
This application is a simple e-commerce application that has 7 endpoints as follows:

| Method | Endpoint                       | Description                                                                                                                      |
|:------:|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
|  POST  | /product                       | Create a new product                                                                                                             |
|  POST  | /product-tag-category          | Create a new product along with tags and category for that product                                                               |
|  POST  | /product-tag-category-coupon   | Create a new product along with tags, categories and coupons for that product                                                    |
|  POST  | /user                          | Create a new user                                                                                                                |
|  POST  | /user-address                  | Create a new user along with the address for that user                                                                           |
|  POST  | /user-address-product          | Create a new user along with the user’s addresses and product sold by that user                                                  |
|  POST  | /user-address-product-shipping | Create a new user along with the user’s addresses and product (along with the shipping method for the product) sold by that user |

## How to Run
I highly recommend running this application using docker compose. The compose file in this code base will run the application server as well as run the MySQL database server so you no longer need to setup the database server manually.

First, create an `.env` file then copy and paste the contents of the `.env.example` file into the `.env` file.

In the `.env` file, there is a `VALIDATION` environment variable that can be filled with 1 of the 5 available validation modes. An explanation of the validation mode value is as follows:

| VALIDATION  | Description                                                               |
|-------------|---------------------------------------------------------------------------|
| no          | Running the application without input validation mechanism                |
| ma-partial | Running the application with partial input validation mechanism using Marshmallow |
| ma-full    | Running the application with full input validation mechanism using Marshmallow    |
| pydantic-partial | Running the application with partial input validation mechanism using Pydantic |
| pydantic-full    | Running the application with full input validation mechanism using Pydantic    |

If you run this application with docker compose then you do not need to change the value of the `DATABASE_URL` environment variable. You may want to change the value of the `DOCKER_PORT` environment variable as the default value is 5000.

To run the application, you can build docker image first with command `docker compose build` or pull the docker image of this application from the docker hub with command `docker compose pull`. Next, run the application with command `docker compose up`.

## Log Files
The application generates 2 log files to record unhandled/unexpected errors and to record application response time. The two log files are as follows:

| Log file path     | Description                      |
|-------------------|----------------------------------|
| logs/err500.log   | logs unhandled/unexpected errors |
| logs/res-time.log | logs application response time   |

## Fuzzing Experiment
If you want to conduct fuzzing experiments on this application, you can use several fuzzing tools such as [Restler](https://github.com/microsoft/restler-fuzzer), [EvoMaster](https://github.com/EMResearch/EvoMaster), [RestTestGen](https://github.com/SeUniVr/RestTestGen), or other tools that can perform fuzzing on RESTful API.

Fuzzing tools usually require OpenAPI specification to generate and send fuzzing payloads to application. You may want to replace the server URL value in the `openapi.json` file as the default value is http://localhost:5000/api

Before carrying out fuzzing experiments, especially experiments with different fuzzing tools and input validation libraries, it is a good idea to delete the `logs` directory first so that the resulting logs match the fuzzing tool and input validation library used.

## Note for Full Validation Mode
In full validation mode, I intentionally do not implement full validation in certain fields, namely regular_price (Product), max_usage (Coupon), and charge (Shipping).

For example, in the Coupon entity, there is max_usage field which has integer data type. I only implement validation against the minimum constraint of the field, which is greater than or equal to 0, and do not implement validation against the maximum constraint of the field. If the client sends max_usage data that exceeds the maximum constraint of the MySQL integer field (4294967295) then the data sent by the client will trigger an error in the application.

This aims to find out whether the fuzzing tool can find these remaining errors.
