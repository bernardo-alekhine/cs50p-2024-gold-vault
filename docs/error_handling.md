# Error Handling

### Description
The [error_handling](/src/gvault/error_handling) package contains the app's base error handler for basic unexpected
behavior in the program's functionality throughout the processes executed by `parser` and `crypto`. As in many command
line interface program's, the error handling was abstracted to mostly exit the program and provide meaningful messages
as for errors that occurred.

Since for sake of simplicity and usage, parsing of arguments or file IO for the sake of the behavior proprosed by
`gvault` didn't display any significant needs to more complex exception handling or error handling.

The `error_handling` package provides an error handling interface for the other packages to use. Including custom
exception classes, error messages and helper classes or modules.
