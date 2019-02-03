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
            //if prommition not denied-exeption

            TcpClient sock = new TcpClient(host, port);
            byte[] data= System.Text.Encoding.ASCII.GetBytes("GETKEY");

            NetworkStream stream = sock.GetStream();
            stream.Write(data, 0, data.Length);

            byte[] bytes = new byte[4];
            int len = int.Parse(System.Text.Encoding.ASCII.GetString(bytes, 0, stream.Read(bytes, 0, 4)));
            bytes = new byte[len];
            string answer =  System.Text.Encoding.ASCII.GetString(bytes, 0, stream.Read(bytes, 0, len));



            if (answer == "DENIED")
                throw new KeyDeniedException();

            return answer;
        }
    }
    class KeyDeniedException : Exception
    {

        public KeyDeniedException() {; }
    }
}

