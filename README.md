# CS3040 SQL runner

This is a script to help you run student submissions (SQL scripts) locally. You neeed Docker to be able to use this script.

## Intalling Oracle db locally

Oracle provides a free tier database in a Docker container. You can follow their instructions [here](https://container-registry.oracle.com/ords/f?p=113:4:16654379714063:::4:P4_REPOSITORY,AI_REPOSITORY,AI_REPOSITORY_NAME,P4_REPOSITORY_NAME,P4_EULA_ID,P4_BUSINESS_AREA_ID:1863,1863,Oracle%20Database%20Free,Oracle%20Database%20Free,1,0&cs=3iImxTsuCNikZaWMqAYuzoEo2OgaxNTh7V5_UV_eLSIFAck0mV3ULJaBbZGoidXzfGLS8qL8qoL37VG8zX_JSsw), or you can use the script I wrote to install it.

```sh
./run_oracledb.sh
```

This script should do the following

1. Pull the Oracle Docker image
2. Start the Oracle database at port number 1521
3. Set the password for the default user `SYS` to `helloworld`

This script is supposed to be idempotent, so if your db is corrupted (For example a student's script left it in a bad state etc) you should be able to just re-run this script and reset your db.

## Downloading student submissions

Say you want to run student John Doe's scripts. Here's how you can do it.

1. Create a folder for him in `submissions` called `john_doe`
2. Manually download John's zip file from Brightspace and place it in the `submissions` folder
3. Unzip all the contents so that John's files are in `submissions/john_doe`

Your file structure should look something like this

```
.
├── main.py
├── pyproject.toml
├── README.md
├── run_oracledb.sh
├── shawn.log
├── submissions
│   ├── john_doe
│   │   ├── HW7-1a.out
│   │   ├── HW7-1a.sql
│   │   ├── HW7-1b.out
│   │   ├── HW7-1b.sql
│   │   ├── HW7-2.out
│   │   ├── HW7-2.sql
│   │   ├── HW7-3.out
│   │   └── HW7-3.sql
│   └── bruce_wayne
│       ├── HW7-1a.out
│       ├── HW7-1a.sql
│       ├── HW7-1b.out
│       ├── HW7-1b.sql
│       ├── HW7-2.out
│       ├── HW7-2.sql
│       ├── HW7-3.out
│       ├── HW7-3.sql
│       └── index.html
│  
└── uv.lock

```

## Running student submissions

Now the fun part. If you haven't used `uv` before I highly recommend using it. I also a added a `requirements.txt` file in case you want to use good ole `pip` to install dependencies. I'll be using `uv run..` in the rest of the doc but you can replace that with just `python  ...` assuming you have all the dependencies installed.

Okay, now that you have John Doe's files in `submissions/john_doe`, you can simply run

```
uv run main.pu john_doe
```

This will combine all of John's SQL files into one script and run it against your local Oracle database. You should be able to see the output, any errors etc in the terminal.
