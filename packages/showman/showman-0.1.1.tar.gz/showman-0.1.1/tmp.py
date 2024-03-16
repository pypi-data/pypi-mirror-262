from pexpect.replwrap import REPLWrapper

try:
    from pexpect import spawn
except ImportError:
    from pexpect.popen_spawn import PopenSpawn as spawn

child = spawn("node -i", encoding="utf-8")
child.echo = False
wrapper = REPLWrapper(child, r"> ", None)

print(wrapper.run_command("x = 1; console.log(x)"))
