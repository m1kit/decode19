import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Set;
import javax.imageio.ImageIO;

/** Starter implementation: compile with `javac Decoder.java`. */
public final class Decoder {
    public record Pixel(int red, int green, int blue) {}

    private static final Set<String> SUPPORTED_TYPES = Set.of(
        "00_braille", "01_morse", "02_code39", "03_pzn", "04_ean13",
        "05_telepen", "06_dx_film_edge", "07_hccb", "08_aztec_rune",
        "09_code128", "10_data_matrix", "11_qr", "12_micro_qr", "13_rmqr",
        "14_aztec", "15_pdf417", "16_micro_pdf417",
        "17_databar_expanded_stacked", "18_maxicode"
    );

    /** Decode a row-major 2-D pixel array and return text without a newline. */
    public static String decode(String codeType, Pixel[][] pixels) {
        throw new UnsupportedOperationException("decoder not implemented for " + codeType);
    }

    private static Pixel[][] loadPixels(String path) throws Exception {
        BufferedImage image = ImageIO.read(new File(path));
        if (image == null) throw new IllegalArgumentException("not a readable image: " + path);
        Pixel[][] pixels = new Pixel[image.getHeight()][image.getWidth()];
        for (int y = 0; y < image.getHeight(); y++) {
            for (int x = 0; x < image.getWidth(); x++) {
                int rgb = image.getRGB(x, y);
                pixels[y][x] = new Pixel((rgb >>> 16) & 255, (rgb >>> 8) & 255, rgb & 255);
            }
        }
        return pixels;
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("usage: java Decoder CODE_TYPE IMAGE_PATH");
            System.exit(2);
        }
        if (!SUPPORTED_TYPES.contains(args[0])) {
            System.err.println("unsupported code type: " + args[0]);
            System.exit(2);
        }
        try {
            System.out.println(decode(args[0], loadPixels(args[1])));
        } catch (Exception error) {
            System.err.println(error.getMessage());
            System.exit(1);
        }
    }
}
