from telethon import events
import asyncio
import io

@Tamokuteki.on(events.NewMessage(pattern = "\.(term|terminal|sh|shell) ", outgoing = True))
async def shell(event):
  if event.fwd_from:
      return
  cmd = event.text.split(" ", 1)
  if len(cmd) == 1: return
  else: cmd = cmd[1]
  async_process =  await asyncio.create_subprocess_shell(cmd, 
      stdout=asyncio.subprocess.PIPE, 
      stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await async_process.communicate()
  msg = f"**Command:**\n`{cmd}`\n"
  if stderr.decode(): msg += f"**Stderr:**\n`{stderr.decode()}`"
  if stdout.decode(): msg += f"**Stdout:**\n`{stdout.decode()}`"
  if len(msg) > 4096:
    with io.BytesIO(msg) as file:
      file.name = "shell.txt"
      await Tamokuteki.send_file(
        event.chat_id,
        file,
        force_document = True,
        caption = cmd,
        reply_to = event.message.id
      )
      return
  await event.edit(msg)


__commands__ = {
  "shell": "Run command"
}
