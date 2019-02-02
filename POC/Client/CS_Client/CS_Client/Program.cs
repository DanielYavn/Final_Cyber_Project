using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace CS_Client
{
    class Program
    {
        static string gameRequest = "GET /game.exe HTTP/1.1\nHost: 192.168.1.134\nConnection: keep-alive\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36\nAccept: */*\nReferer: \nAccept-Encoding: gzip, deflate\nAccept-Language: en-US";

        static void Main(string[] args)
        {
            string serverIP = "192.168.1.134";
            int ServerPort = 50001;

            byte[] bytes = new Byte[1024];
            IPHostEntry ipHostInfo = Dns.Resolve(serverIP);
            IPAddress ipAddress = ipHostInfo.AddressList[0];
            IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 50001);

            Socket sender = new Socket(AddressFamily.InterNetwork,
SocketType.Stream, ProtocolType.Tcp);
            sender.Connect(localEndPoint);
            byte[] msg = Encoding.ASCII.GetBytes(gameRequest);
            int bytesSent = sender.Send(msg);
            int bytesRec = sender.Receive(bytes);
            string answer=Encoding.ASCII.GetString(bytes, 0, bytesRec);
            sender.Shutdown(SocketShutdown.Both);
            sender.Close();

            string path = Directory.GetCurrentDirectory()+@"\game.exe";
            Console.WriteLine(path);
            //if (!File.Exists(path))
            {
                // Create a file to write to.
                using (StreamWriter sw = File.CreateText(path))
                {
                    sw.WriteLine(answer);
                    
                }
            }

        }
    }
}
