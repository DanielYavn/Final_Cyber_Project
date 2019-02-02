using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;

namespace Client
{
    class Communication
    {
        public static int port = 50001;
        public static string host = "192.168.1.134";

        public static string GetEKey()
        {
            //if prommition not granted exeption

            TcpClient sock = new TcpClient(host, port);
            byte[] data= System.Text.Encoding.ASCII.GetBytes("GETKEY");

            NetworkStream stream = sock.GetStream();
            Console.WriteLine("sent: GETKEY");
            stream.Write(data, 0, data.Length);


            string answer = System.Text.Encoding.ASCII.GetString(data, 0, stream.Read(data, 0, data.Length));
            Console.WriteLine("ans: "+ answer);
            return answer;
        }


    }
}
