using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;
using System.Reflection;

namespace Client
{
    class RunGame
    {
        public static void RunCSExe(byte[] code)
        {
            //byte[] bin = Encoding.ASCII.GetBytes(code);
            ///////////////////////////

            FileStream fs = new FileStream(@"..\SimpleGame.exe", FileMode.Open);
            BinaryReader br = new BinaryReader(fs);
            byte[] bin2 = br.ReadBytes(Convert.ToInt32(fs.Length));
            for (int i = 0; i < code.Length; i++)
            {
                if (code[i]!=bin2[i])
                    Console.WriteLine(code[i] + " "+bin2[i]+" index " +i);
            }
            fs.Close();
            br.Close();
            ///////////////////
            Assembly a = Assembly.Load(code);
            MethodInfo method = a.EntryPoint;

            if (method != null)
            {
                object o = a.CreateInstance(method.Name);
                
                method.Invoke(o, new object[] {new string[0] });
            }
        }
    }
}

            
            
           
