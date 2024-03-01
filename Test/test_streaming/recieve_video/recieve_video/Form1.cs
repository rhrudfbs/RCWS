using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Windows.Forms;
using System.Threading;
using System.Security.Cryptography;

namespace recieve_video
{
    public partial class Form1 : Form
    {
        String IPaddress_;
        int Port_;
        UdpClient udpClient;
        IPEndPoint endPoint;

        public Form1()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            IPaddress_ = textBox1.Text;
            Port_ = Int32.Parse(textBox2.Text);
            StartReceiving(IPaddress_, Port_);
        }

        private void StartReceiving(string ip, int port)
        {
            udpClient = new UdpClient(Port_);
            //udpClient.Client.ReceiveBufferSize = 65540; // 수신 버퍼 크기를 65540으로 조정
            endPoint = new IPEndPoint(IPAddress.Parse(ip), Port_);

            // 비동기적으로 데이터 수신 시작
            udpClient.BeginReceive(new AsyncCallback(ReceiveCallback), null);
        }

        private void Showvideo(byte[] Data_)
        {
            this.Invoke((MethodInvoker)delegate
            {
                try
                {
                    //수신된 데이터로부터 이미지 생성
                    using (var ms = new MemoryStream(Data_))
                    {
                        var receivedImage = Image.FromStream(ms);

                        //PictureBox에 이미지 표시
                        pictureBox1.Image = receivedImage;
                    }
                }
                catch (Exception ex)
                {
                    // 이미지 처리 중 오류 발생 처리
                    listBox1.Items.Add("Error displaying image: " + ex.Message);
                    listBox1.Items.Add(Data_.Length);
                }
            });
        }

        private void ReceiveCallback(IAsyncResult ar)
        {
            byte[] receivedData = udpClient.EndReceive(ar, ref endPoint);
            //string receivedMessage = Encoding.ASCII.GetString(receivedData);

            if (receivedData.Length < 65000)
            {
                Showvideo(receivedData);
            }
            else
            {
                byte[] dgram = udpClient.Receive(ref endPoint);
                if (dgram.Length < 65000)
                {
                    Showvideo(receivedData.Concat(dgram).ToArray());
                }
                else
                {
                    byte[] dgram_ = receivedData.Concat(dgram).ToArray();
                    byte[] dgram__ = udpClient.Receive(ref endPoint);
                    Showvideo(dgram_.Concat(dgram__).ToArray());
                }
            }
            // 비동기 수신을 계속하기 위해 다시 시작
            udpClient.BeginReceive(new AsyncCallback(ReceiveCallback), null);
        }
    }
}