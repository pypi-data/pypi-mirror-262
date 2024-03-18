# CloudTeam_Logger

## Table of Contents

- [About](#about)
- [Usage](#usage)
- [Functions](../function.md)

## About <a name = "about"></a>

This module is a logger module for cloudteam to simplify the logging process

## Usage <a name = "usage"></a>

in you code write the following line:    
```
import cloudteam_logger
log = cloudteam_logger.ct_logger(<"the folder which you want the logs to be greated">,<optional: mode='debug'>)
log.<WANTED FUNCTION>("your log")
```

## Functions <a name = "function"></a>
- INFO - log level info
- ERROR - log level error
- WARNING - log level warning
- CRITICAL - log level critical
- DEBUG - only shown when mode = debug, log level debug