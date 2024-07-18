import copy
from typing import List
from hardware.ssd_common_data import CMD_WRITE_TYPE, CMD_ERASE_TYPE, MAX_ERASE_SIZE


class BufferOptimizer:
    def optimize_command_buffer(self, buffer: List[List[str]]):
        size = len(buffer)
        optimized_buffer = copy.copy(buffer)
        for i in range(size - 1):
            cur_idx = size - 1 - i
            self._optimize_if_prev_command_editable(cur_idx, optimized_buffer)
            self._optimize_if_prev_command_useless(cur_idx, optimized_buffer)
            self._optimize_if_prev_command_mergable(cur_idx, optimized_buffer)
        optimized_buffer = [e for e in optimized_buffer if e is not None]
        return optimized_buffer

    def _optimize_if_prev_command_mergable(self, cur_idx: int, command_buffer: List):
        cur_cmd = command_buffer[cur_idx]
        prev_cmd = command_buffer[cur_idx - 1]
        if (cur_cmd is None) or (prev_cmd is None):
            return
        cur_cmd_type = cur_cmd[0]
        prev_cmd_type = prev_cmd[0]
        if cur_cmd_type != CMD_ERASE_TYPE or prev_cmd_type != CMD_ERASE_TYPE:
            return
        cur_start_addr = int(cur_cmd[1])
        cur_end_addr = cur_start_addr + int(cur_cmd[2])
        prev_start_addr = int(prev_cmd[1])
        prev_end_addr = prev_start_addr + int(prev_cmd[2])

        if prev_end_addr == cur_start_addr and (cur_end_addr - prev_start_addr) <= MAX_ERASE_SIZE:
            command_buffer[cur_idx - 1] = ['E', str(prev_start_addr), str(cur_end_addr - prev_start_addr)]
            command_buffer[cur_idx] = None
        elif cur_end_addr == prev_start_addr and (prev_end_addr - cur_start_addr) <= MAX_ERASE_SIZE:
            command_buffer[cur_idx - 1] = ['E', str(cur_start_addr), str(prev_end_addr - cur_start_addr)]
            command_buffer[cur_idx] = None

    def _optimize_if_prev_command_useless(self, cur_idx: int, command_buffer: List):
        cur_cmd = command_buffer[cur_idx]
        if cur_cmd is None:
            return
        for i in range(cur_idx):
            prev_cmd = command_buffer[i]
            if prev_cmd is None:
                continue
            if self._check_erasable(cur_cmd, prev_cmd):
                command_buffer[i] = None

    def _optimize_if_prev_command_editable(self, cur_idx: int, command_buffer: List):
        cur_cmd = command_buffer[cur_idx]
        if cur_cmd is None:
            return
        for i in range(cur_idx):
            prev_cmd = command_buffer[i]
            if (prev_cmd is None) or (prev_cmd[0] != CMD_ERASE_TYPE) or (cur_cmd[0] != CMD_WRITE_TYPE):
                continue
            cur_cmd_addr = int(cur_cmd[1])
            prev_cmd_addr = int(prev_cmd[1])
            prev_erase_size = int(prev_cmd[2])
            if cur_cmd_addr == prev_cmd_addr and prev_erase_size > 1:
                prev_cmd[1] = str(prev_cmd_addr + 1)
                prev_cmd[2] = str(prev_erase_size - 1)
            elif cur_cmd_addr == (prev_cmd_addr + prev_erase_size - 1):
                prev_cmd[2] = str(prev_erase_size - 1)

    def _check_erasable(self, cur_cmd: List[str], prev_cmd: List[str]):
        cur_cmd_type = cur_cmd[0]
        cur_cmd_addr = int(cur_cmd[1])
        prev_cmd_type = prev_cmd[0]
        prev_cmd_addr = int(prev_cmd[1])
        if cur_cmd_type == CMD_WRITE_TYPE and prev_cmd_type == CMD_WRITE_TYPE:
            if self._check_erasable_when_both_write(cur_cmd_addr, prev_cmd_addr):
                return True
        elif cur_cmd_type == CMD_WRITE_TYPE and prev_cmd_type == CMD_ERASE_TYPE:
            if self._check_erasable_when_cur_write_prev_erase(cur_cmd_addr, prev_cmd_addr, int(prev_cmd[2])):
                return True
        elif cur_cmd_type == CMD_ERASE_TYPE and prev_cmd_type == CMD_WRITE_TYPE:
            if self._check_erasable_when_cur_erase_prev_write(cur_cmd_addr, int(cur_cmd[2]), prev_cmd_addr):
                return True
        elif cur_cmd_type == CMD_ERASE_TYPE and prev_cmd_type == CMD_ERASE_TYPE:
            if self._check_erasable_when_both_erase(cur_cmd_addr, int(cur_cmd[2]), prev_cmd_addr, int(prev_cmd[2])):
                return True
        return False

    def _check_erasable_when_both_write(self, cur_cmd_addr, prev_cmd_addr):
        return prev_cmd_addr == cur_cmd_addr

    def _check_erasable_when_cur_write_prev_erase(self, cur_cmd_addr, prev_cmd_addr, prev_erase_size):
        return cur_cmd_addr == prev_cmd_addr and prev_erase_size <= 1

    def _check_erasable_when_cur_erase_prev_write(self, cur_cmd_addr, cur_erase_size, prev_cmd_addr):
        return cur_cmd_addr <= prev_cmd_addr < cur_cmd_addr + cur_erase_size

    def _check_erasable_when_both_erase(self, cur_cmd_addr, cur_erase_size, prev_cmd_addr, prev_erase_size):
        return (cur_cmd_addr <= prev_cmd_addr) and \
            ((prev_cmd_addr + prev_erase_size) <= (cur_cmd_addr + cur_erase_size))
