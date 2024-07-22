# SSD - Team BuildBetter

_**2024 7th CRA Team project**_

## Collaborators
- 강동현: 팀장, BasicLogic, TestApps / Runner 기능, 재빌드 이슈 해결
- 김정훈: 발표, BasicLogic, TestApps / Runner 기능, 재빌드 이슈 해결
- 김지훈: 시연, Stdin 처리 (Test Shell) / Logger 기능
- 박준혁: SSD read/write/erase/flush 기능 개발 / Command Buffer 기능
- 조병덕: SSD read/write/erase/flush 기능 개발 / Command Buffer 기능 
- 최아련: Stdin 처리 (Test Shell) / Logger 기능

## Usage

- TestShell 사용이 권장됩니다.

### SSD
```chatinput
> python hardware/ssd.py R 1
```

### TestShell
```chatinput
> python .\app\ssd_test_shell.py
help
********************* COMMAND HELP ***********************
- exit: Exit program / usage: exit
- help: Help command
- write: Write value to SSD / usage: write <LBA> <VALUE>
- read: Read value from SSD / usage: read <LBA>
- fullread: Read all LBAs / usage: fullread
- fullwrite: Write value at all LBAs / usage: fullwrite <VALUE>
- erase: Erase value of SIZE from LBA on SSD / usage : erase <LBA> <SIZE>
- erase_range: Erase value from startLBA to endLBA on SSD / usage : erase_range <Start LBA>  <End LBA>
- flush: flush command buffer of SSD / usage: flush
- Available Tests
   * fail_test
   * fullwrite_erase_read_compare
   * fullwrite_read_compare
   * write_10times_overwrite_read_compare
*********************************************************
```