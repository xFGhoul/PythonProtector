## 1.0 - 2022-09-18

Release Initial Project

## 1.1 - 2022-12-28

So It's been kind of a while since we released a new update, I had some pretty big stuff going on irl, no time to code, just recently came back and decided to make some updates.

- Completely Configurable Module System - Users now have the choice of deciding what modules they use, currently there are only the main 4 me and marci provide, but we are open to pull requests and we will be adding more in the future, do check the repository or the example for more information.

- `should_exit` argument - gives users the ability to decide if the program should exit if one of the detections were raised.

- Overall Improvement/Refactoring - This update didn't bring everything me and marci are planning for, but this is just a couple, in the update I made to sure to cover some edge cases so you guys don't get confused

## 1.5 - 2022-01-05

I know this is a pretty quick release, and the jump from `1.1` to `1.5` but I felt it was only necessary with the amount of changes made.

### Major Changes:

- **Encrypted Logging** - Instead of logs that anybody can read, logs are now encrypted at runtime and are only decrypted if malicious activity is detected

- **AntiAnalysis** - Thanks to the work of Marci, a new module has been made!, this one comes with some pretty neat features, be sure to check it out

- **New On Detection System** / `on_detect` - Similarly to the new configurable module system, I've gone ahead and done the same with what happens when malicious activity is detected, check out the examples for how it's used

### Minor Changes

- **Updated Minimum Python Requirement To 3.11**

- **Refactoring and Misc Improvements**