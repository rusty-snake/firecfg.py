use std::env;
use std::ffi::OsStr;
use std::os::unix::process::CommandExt;
use std::path::Path;
use std::path::PathBuf;
use std::process::Command;

struct Cmdl<T, U> {
    program: T,
    args: U,
}

fn main() -> ! {
    let (mut _cmdl_a, mut _cmdl_b);
    let cmdl: Cmdl<&dyn AsRef<OsStr>, &mut dyn Iterator<Item = String>>;
    if let Ok("firejail") = env::var("container").as_deref() {
        let arg0 = env::args().next().unwrap();
        let program_name = Path::new(&arg0).file_name().unwrap();

        _cmdl_a = Cmdl {
            program: find_program(program_name)
                .unwrap_or_else(|| panic!("Could not find '{}'", program_name.to_string_lossy())),
            args: env::args().skip(1),
        };
        cmdl = Cmdl {
            program: &_cmdl_a.program,
            args: &mut _cmdl_a.args,
        };
    } else {
        _cmdl_b = Cmdl {
            program: "firejail",
            args: env::args(),
        };
        cmdl = Cmdl {
            program: &_cmdl_b.program,
            args: &mut _cmdl_b.args,
        };
    }

    let err = Command::new(cmdl.program).args(cmdl.args).exec();
    panic!("Failed to exec child: {}", err);
}

fn find_program<P: AsRef<Path>>(program_name: P) -> Option<PathBuf> {
    env::var("PATH")
        .expect("Failed to get $PATH")
        .split(':')
        .filter(|path| !path.contains("firecfg.py"))
        .map(|path| Path::new(path).join(&program_name))
        .find(|path| path.exists())
}
