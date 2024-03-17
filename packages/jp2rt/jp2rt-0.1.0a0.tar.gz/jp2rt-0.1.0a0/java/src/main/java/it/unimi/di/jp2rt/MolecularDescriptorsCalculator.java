package it.unimi.di.jp2rt;

import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Objects;
import java.util.stream.Stream;

import me.tongfei.progressbar.ProgressBar;
import me.tongfei.progressbar.ProgressBarBuilder;

public class MolecularDescriptorsCalculator {

  private MolecularDescriptorsCalculator() {};

  public static long numLines(String filename) throws IOException {
    final byte[] buffer = new byte[8192];
    int n, count = 0;
    try (FileInputStream stream = new FileInputStream(filename)) {
      while ((n = stream.read(buffer)) > 0) {
        for (int i = 0; i < n; i++)
          if (buffer[i] == '\n')
            count++;
      }
    }
    return count;
  }

  private static class ThreadSafeCalculator {
    private static final ThreadLocal<MolecularDescriptorsWrapper> descriptorsHolder = new ThreadLocal<>() {
      @Override
      protected MolecularDescriptorsWrapper initialValue() {
        return new MolecularDescriptorsWrapper();
      };
    };

    public static TSVLine calculate(final String smiles) {
      return descriptorsHolder.get().calculate(new TSVLine(smiles));
    }
  }

  public static Stream<TSVLine> fromStream(final Stream<String> stream, final ProgressBarBuilder pbb) {
    Objects.requireNonNull(stream, "Stream cannot be null");
    return pbb == null ? stream.map(ThreadSafeCalculator::calculate)
        : ProgressBar.wrap(stream, pbb).map(ThreadSafeCalculator::calculate);
  }
 
  public static Stream<TSVLine> fromFile(final String inPath, final ProgressBarBuilder pbb) throws IOException {
    Path p = Paths.get(Objects.requireNonNull(inPath, "Input file cannot be null"));
    if (!(p.toFile().isFile() && p.toFile().canRead()))
    throw new IllegalArgumentException("Input file does not exist or is not readable");
    return fromStream(Files.lines(p).parallel(), pbb);
  }
  
  public static Stream<TSVLine> fromFile(final String inPath) throws IOException {
    ProgressBarBuilder pbb = new ProgressBarBuilder();
    pbb.setInitialMax(numLines(inPath)).setTaskName("Computing");
    return fromFile(inPath, pbb);
  }
  
  public static Stream<TSVLine> fromList(final List<String> list, final ProgressBarBuilder pbb) {
    Objects.requireNonNull(list, "List cannot be null");
    return fromStream(list.stream().parallel(), pbb);
  }

  public static void toFile(final Stream<TSVLine> stream, final String outPath) throws IOException {
    Objects.requireNonNull(stream, "Stream cannot be null");
    try (PrintWriter ps = new PrintWriter(new BufferedOutputStream(new FileOutputStream(outPath))) ) {
      stream.forEach(ps::println);
    }
  }

  public static void main(String[] args) throws IOException {

    final String help = "Usage: jp2rt --list-descriptors | -l, or DescriptorsCalculator <input file> <output file>";

    if (args.length == 1) {
      System.out.println(args[0].equals("--list-descriptors") || args[0].equals("-l") ? new MolecularDescriptorsWrapper() : help);
      System.exit(0);
    } else if (args.length != 2) {
      System.err.println(help);
      System.exit(1);
    } 
    toFile(fromFile(args[0]), args[1]);

  }
}
