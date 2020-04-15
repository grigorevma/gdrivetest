from sanic.response import StreamingHTTPResponse, guess_type, path
from app.core import session_boto as sb
from app.config import bucket, AWS_IDKEY, AWS_SKEY


async def file_boto_stream(
    data=None,
    location=None,
    status=200,
    chunk_size=4096,
    mime_type=None,
    headers=None,
    filename=None,
    chunked=True,
    _range=None,
):
    """Return a streaming response object with file data.

    :param location: Location of file on system.
    :param chunk_size: The size of each chunk in the stream (in bytes)
    :param mime_type: Specific mime_type.
    :param headers: Custom Headers.
    :param filename: Override filename.
    :param chunked: Enable or disable chunked transfer-encoding
    :param _range:
    """
    headers = headers or {}
    if filename:
        headers.setdefault(
            "Content-Disposition", 'attachment; filename="{}"'.format(filename)
        )
    filename = filename or path.split(location)[-1]

    async def _streaming_fn(response):

        async with sb.create_client('s3', region_name='eu-central-1',
                                    aws_secret_access_key=AWS_SKEY,
                                    aws_access_key_id=AWS_IDKEY) as cl:
            resp = await cl.get_object(Bucket=bucket, Key=filename)

            try:
                while True:
                    content = await resp['Body'].read(4096)
                    if len(content) < 1:
                        break
                    await response.write(content)
            except Exception as e:
                print("-------- its error ------------")
                print(e)
            return  # Returning from this fn closes the stream

    mime_type = mime_type or guess_type(filename)[0] or "text/plain"
    if _range:
        headers["Content-Range"] = "bytes %s-%s/%s" % (
            _range.start,
            _range.end,
            _range.total,
        )
        status = 206
    return StreamingHTTPResponse(
        streaming_fn=_streaming_fn,
        status=status,
        headers=headers,
        content_type=mime_type,
        chunked=chunked,
    )
