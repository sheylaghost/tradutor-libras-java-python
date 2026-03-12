import org.bytedeco.javacv.*;
import org.bytedeco.opencv.opencv_core.*;
import static org.bytedeco.opencv.global.opencv_core.*;
import static org.bytedeco.opencv.global.opencv_imgproc.*;

import java.io.*;
import java.net.Socket;

public class libras {
    public static void main(String[] args) throws Exception {

        // Conecta ao Python via socket
        Socket socket = new Socket("localhost", 9999);
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        System.out.println("Conectado ao Python!");

        // Camera DroidCam
        FFmpegFrameGrabber grabber = new FFmpegFrameGrabber("http://192.168.0.23:4747/video");
        grabber.setFormat("mjpeg");
        grabber.setImageWidth(640);
        grabber.setImageHeight(480);
        grabber.setOption("analyzeduration", "1000000");
        grabber.setOption("probesize", "10000000");
        grabber.start();

        CanvasFrame canvas = new CanvasFrame("Tradutor de Libras");
        canvas.setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE);
        OpenCVFrameConverter.ToMat converter = new OpenCVFrameConverter.ToMat();

        while (canvas.isVisible()) {
            Frame frame = grabber.grab();
            if (frame == null || frame.image == null) continue;

            Mat mat = converter.convert(frame);
            if (mat == null || mat.empty()) continue;

            // Le os pontos da mao enviados pelo Python
            String linha = reader.readLine();

            if (linha != null && !linha.equals("NENHUMA_MAO")) {
                String[] pontos = linha.split(";");
                for (String ponto : pontos) {
                    String[] xy = ponto.split(",");
                    int x = (int)(Float.parseFloat(xy[0]) * mat.cols());
                    int y = (int)(Float.parseFloat(xy[1]) * mat.rows());
                    circle(mat, new Point(x, y), 6, new Scalar(0, 255, 0, 0), -1, 8, 0);
                }
                putText(mat, "Mao detectada!", new Point(10, 50),
                        FONT_HERSHEY_SIMPLEX, 1.2,
                        new Scalar(0, 255, 0, 0), 2, LINE_8, false);
            } else {
                putText(mat, "Nenhuma mao", new Point(10, 50),
                        FONT_HERSHEY_SIMPLEX, 1.2,
                        new Scalar(0, 0, 255, 0), 2, LINE_8, false);
            }

            canvas.showImage(converter.convert(mat));
        }

        grabber.stop();
        canvas.dispose();
        socket.close();
    }
}
