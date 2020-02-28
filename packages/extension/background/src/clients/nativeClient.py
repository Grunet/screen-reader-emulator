from lib.src.stdToStreams import convertStdToRxStreams


def connectToExtension(nativeAppStdin, nativeAppStdout):
    return convertStdToRxStreams(nativeAppStdin, nativeAppStdout)
