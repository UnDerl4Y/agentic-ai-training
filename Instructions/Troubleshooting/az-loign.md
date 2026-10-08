## Troubleshooting

### Q1. I ran `az login`, but I can't see the sign-in window.

**A.** The Azure sign-in window may be hidden behind another application or browser window in the VM.

Try the following:

1. Minimize all open applications and browser windows.
2. Look for the Microsoft sign-in window running in the background.
3. Select **Work or school account** and sign in using the credentials provided by your instructor.
4. Complete the sign-in process.

> [!TIP]
> If `az login` appears to do nothing, the sign-in window may be hidden behind another window in the VM.

### Q2. I am experiencing issues after running `az login`.

**A.** Clear the current Azure CLI session and sign in again.

1. Run:

   ```powershell
   az logout
   ```

2. Sign in again:

   ```powershell
   az login
   ```

3. Verify that the login was successful:

   ```powershell
   az account show
   ```

If account details are displayed, you are successfully authenticated and can continue with the lab.