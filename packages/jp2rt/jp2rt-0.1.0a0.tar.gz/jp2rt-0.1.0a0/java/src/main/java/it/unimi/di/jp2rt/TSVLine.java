package it.unimi.di.jp2rt;

import java.util.Objects;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;

public class TSVLine {
    private final String[] extra;
    private final String smiles;
    private DoubleStream descriptors = null;

    public TSVLine(final String line) {
      final String[] fields = Objects.requireNonNull(line, "The line parameter must not be null").split("\t");
      extra = Arrays.copyOfRange(fields, 0, fields.length - 1);
      smiles = fields[fields.length - 1];
      if (smiles.isBlank()) throw new IllegalArgumentException("The SMILES string (last field on the line) must not be blank");
    }

    public List<String> extra() {
      return Arrays.asList(extra);
    }

    public String smiles() {
      return smiles;
    }

    public double[] descriptors() {
      return descriptors.toArray();
    }

    public TSVLine descriptors(DoubleStream values) {
      this.descriptors = Objects.requireNonNull(values, "The values parameter must not be null");
      return this;
    }

    @Override
    public String toString() {
      return (extra.length > 0 ? String.join("\t", extra) + "\t" : "" )+ smiles + (descriptors != null ? "\t" + descriptors.mapToObj(Double::toString).collect(Collectors.joining("\t")) : "");
    }
  }

