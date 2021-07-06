/*
 * Copyright © 2021 The firecfg.py Authors
 *
 * This file is part of firecfg.py
 *
 * firecfg.py is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * firecfg.py is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

use std::env;
use std::os::unix::process::CommandExt;
use std::path::Path;
use std::path::PathBuf;
use std::process::exit;
use std::process::Command;
use std::io::Error as IoError;

fn main() -> ! {
    let mut args /*: impl Iterator<Item = String> */ = env::args();
    let arg0: String = args.next().unwrap();

    let mut command: Command;
    if let Ok("firejail") = env::var("container").as_deref() {
        let program_name: &str = basename(&arg0).unwrap();
        let program: PathBuf = find_program(program_name).unwrap_or_else(|| {
            eprintln!("maybe-firejail: Could not find '{}'", program_name);
            exit(1);
        });

        command = Command::new(program);
    } else {
        assert!(!arg0.starts_with('-'));

        command = Command::new("firejail");
        command.arg(arg0);
    };

    let err: IoError = command.args(args).exec();
    eprintln!("maybe-firejail: Failed to exec child: {}", err);
    exit(1);
}

fn basename(path: &str) -> Option<&str> {
    path.rsplit_once('/').map(|(_, file_name)| file_name)
}

fn find_program<P: AsRef<Path>>(program_name: P) -> Option<PathBuf> {
    env::var("PATH")
        .expect("Failed to get $PATH")
        .split(':')
        .filter(|path| !path.starts_with('/'))
        .filter(|path| !path.contains("firecfg.py"))
        .map(|path| Path::new(path).join(&program_name))
        .find(|path| path.exists())
}
