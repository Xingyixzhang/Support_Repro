using Sender;
using Sender.Models;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace WeatherApp
{
    public class Program
    {
        public static string ConnectionString = "YourEHConnectionStringWithEntityName";

        static void Main(string[] args)
        {
            SenderHelper helper = new SenderHelper(ConnectionString);
            
            for(int i = 0; i < 5; i++) // execution iterations
            {
                helper.DataSender();
                Thread.Sleep(1500); // <=200 ms is not working. 1500> x >=300 executed but not exactly in steps. Doesn't matter how many times the loop ran.
            }
        }
    }
}
