# chorebot

For chore rotation at hackerspaces

## Usage

**Prerequisites:**

* Chores that need to be done each week
* >1 Human beings on a mailing list
* [Mailgun](https://www.mailgun.com/) account

**Configuration:**

Something like this should go in config.json in the same directory as the script:

```
{
  "robot_name": "Chorebot",
  "hackerspace_mailing_list": "members@pettyimperialbrokerage.com",
  "subject_line": "Chores",
  "actuators": [
    "Alice",
    "Bob",
    "Eve",
  ],
  "api_key": "key-sldfskjhaljfaldvb",
  "mailgun_domain": "sandbox4kjfahskjhkbvskjdkf.mailgun.org"
}
```
