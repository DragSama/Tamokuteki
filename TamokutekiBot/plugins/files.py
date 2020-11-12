from TamokutekiBot.helpers import command, format_bytes

@Tamokuteki.on(command(pattern="download"))
async def download_file(event):
    if not event.is_reply:
        await event.edit('Format: .download <As reply>')
        return
    reply= await event.get_reply_message()
    try:
        path = await Tamokuteki.download_media(
            reply,
            'Downloads/',
            progress_callback = lambda current, total: event.edit(f'Downloaded {format_bytes(current)} out of {format_bytes(total)} ')
        )
    except Exception as e:
        await event.edit(f'An error occurred:\n{str(e)}')
        return
    await event.edit(f"Successfully downloaded to {path}")

__commands__ = {
    'download': 'Download a file. <As reply>'
}
