# Project427
Done by 
1. Omar Alabdali
2. Almuhanad Alghaithi
3. Haitham Albrashdi

There were 6 commands used in this program which were:
- Login: login helps the clients to access the server.
- Solve: When the clients get access to the server, they can use solve for either solving for rectangles or for circles, which it distinguishes by the -c and -r flags.
- List: It returns all the solutions that were requested by the user.
- Message: Allow each client to be able to contact any of the other clients. Additionally, the root has special broadcast privileges that sends to all clients that logged in.
- Shutdown: the shutdown command terminates all open sockets and files
- Logout: as the shutdown terminates all open sockets and files the logout command will terminate the clients only.

To run this program, you should run the clients and the server programs simultaneously, then the clients will get access to the server. Also, the server allows multiple clients to be connected simultaneously, and the server know which client is which. At first the clients should Login to get access to the other commands by entering his username and password, then they can access the commands by entering the specific command that they want. (Ex: SOLVE -c 5). They can use the solve of list command as much as they want until they execute the logout or shutdown commands which will no longer give them access to the server. To run the commands they should be typed in in capital letters

There are two bugs are noticeable. First bug happened when one of the users input “SHUTDOWN”, the server crashed! The second bug happened when the user sends a message to another client, the other client doesn’t receive it until the user writes a command or press enter. This is due that the receiver is on the sending statue, so he must enter the receiving statue to receive the message

#Screenshots

<img width="399" alt="image" src="https://user-images.githubusercontent.com/103977763/163912581-fb597f27-b33a-48e2-9361-30c466e89104.png">
<img width="401" alt="image" src="https://user-images.githubusercontent.com/103977763/163912609-7811c7fd-1cbe-44e1-9921-166eafc0d722.png">
<img width="232" alt="image" src="https://user-images.githubusercontent.com/103977763/163912617-f3c27a38-542e-48ef-b9b6-0045d09b7c91.png">
<img width="418" alt="image" src="https://user-images.githubusercontent.com/103977763/163912621-049d2964-18c2-4ec9-aa4a-8a5e59065a00.png">
<img width="364" alt="image" src="https://user-images.githubusercontent.com/103977763/163912633-08ae6932-962c-4083-bdf0-b94d8c20297a.png">
<img width="366" alt="image" src="https://user-images.githubusercontent.com/103977763/163912635-ed23fda5-fa91-4eb2-9c4f-9873c4666268.png">
<img width="229" alt="image" src="https://user-images.githubusercontent.com/103977763/163912724-401dc03b-2566-4eac-9c2d-f72fdaf56fe8.png">
<img width="484" alt="image" src="https://user-images.githubusercontent.com/103977763/163912729-3d9c4c26-2430-456e-8d96-2a0e94a637e3.png">
<img width="468" alt="image" src="https://user-images.githubusercontent.com/103977763/163912738-a6b7e29d-f963-4445-8d41-7ae3a907c95f.png">
<img width="352" alt="image" src="https://user-images.githubusercontent.com/103977763/163912743-ef214192-ca88-4346-a997-5ef6b96ce79c.png">
<img width="229" alt="image" src="https://user-images.githubusercontent.com/103977763/163912724-401dc03b-2566-4eac-9c2d-f72fdaf56fe8.png">
<img width="275" alt="image" src="https://user-images.githubusercontent.com/103977763/163912756-85199c2e-7e4c-4349-ab4b-6b3235fa1dbc.png">
<img width="287" alt="image" src="https://user-images.githubusercontent.com/103977763/163912759-786221ce-02ab-4aa9-a3dd-2fbea4961e5a.png">
