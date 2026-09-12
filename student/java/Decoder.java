import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Set;
import javax.imageio.ImageIO;

/** Starter implementation: compile with `javac Decoder.java`. */
public final class Decoder {
    public record Pixel(int red, int green, int blue) {}

    private static final Set<String> SUPPORTED_TYPES = Set.of(
        "japanese_braille", "morse", "code39", "pzn", "ean13", "telepen",
        "dx_film_edge", "hccb", "aztec_rune", "code128",
        "data_matrix", "qr", "micro_qr", "rmqr", "aztec", "pdf417",
        "micro_pdf417", "databar_expanded_stacked", "maxicode"
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
