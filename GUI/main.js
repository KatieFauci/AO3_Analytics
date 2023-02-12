eel.expose(printToOutput);
function printToOutput(output) {
    console.log("IN JAVASCRIPT PRINT FUNCTION");
    document.getElementById("output-box").value = document.getElementById("output-box").value + "\n" + output;
}