# Download only the VinDr-CXR test folder on Windows

Run in PowerShell from the repository root. GNU Wget is installed locally at
`.tools/wget/wget.exe`; bare `wget` resolves to PowerShell's Invoke-WebRequest
on this machine. No global PATH or PowerShell profile change is required.

```powershell
$physionetUser = Read-Host 'PhysioNet username'
.\.tools\wget\wget.exe --no-config --recursive --level=inf --no-parent --continue --no-host-directories --cut-dirs=3 --https-only --reject="index.html*" --directory-prefix="data/raw/vindr-cxr" --user="$physionetUser" --ask-password "https://physionet.org/files/vindr-cxr/1.0.0/test/"
```

Enter the password at Wget's terminal prompt, never in chat or the command line.
Files land in `data/raw/vindr-cxr/test/` (Git-ignored). Change
`--directory-prefix` to another drive/folder if needed; keep that destination
unchanged when resuming. Stop with Ctrl+C and rerun the same command to resume.
`--continue` resumes partial files; it does not verify checksums or repair
previously corrupted files. Review the final Wget exit status and errors.

The starting URL and `--no-parent` restrict traversal to the test subtree.
Directory listing HTML may be fetched for traversal but is rejected from the
saved dataset. Training images and the separate annotations folder are outside
this scope. The [dataset documentation](https://physionet.org/content/vindr-cxr/1.0.0/)
describes 3,000 test images and separate annotation CSV files. It also requires
credentialing, the specified training, and signing the project's data use
agreement. If authentication fails, first confirm that the same account can
open the test folder in a browser. A browser login does not log Wget in.

## Installation and verification (2026-09-16)

Downloaded the x64 standalone GNU Wget 1.21.4 binary over verified HTTPS from
the [Windows port maintainer](https://eternallybored.org/misc/wget/):

```powershell
New-Item -ItemType Directory -Force .tools\wget | Out-Null
curl.exe --fail --location --output .tools\wget\wget.exe https://eternallybored.org/misc/wget/1.21.4/64/wget.exe
.\.tools\wget\wget.exe --no-config --version
Get-FileHash .tools\wget\wget.exe -Algorithm SHA256
.\.tools\wget\wget.exe --no-config --spider --timeout=20 --tries=1 https://physionet.org/files/vindr-cxr/1.0.0/test/
```

Observed SHA256 (local provenance, not an independently published checksum):
`6136e66e41acd14c409c2d3eb10d48a32febaba04267303d0460ed3bee746cc5`.
`--no-config` avoids the maintainer-documented system wgetrc loading issue.
TLS certificate verification remains enabled. The unauthenticated probe
connected successfully and received HTTP 401, as expected for restricted files.
Authenticated access, disk capacity, and dataset completion remain unverified;
no dataset files were downloaded during setup.
