package it.unimi.di.jp2rt;

import java.util.Objects;
import java.util.function.Function;
import java.util.function.IntToDoubleFunction;
import java.util.logging.Logger;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;

import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.qsar.DescriptorValue;
import org.openscience.cdk.qsar.IMolecularDescriptor;
import org.openscience.cdk.qsar.result.BooleanResult;
import org.openscience.cdk.qsar.result.DoubleArrayResult;
import org.openscience.cdk.qsar.result.DoubleResult;
import org.openscience.cdk.qsar.result.IDescriptorResult;
import org.openscience.cdk.qsar.result.IntegerArrayResult;
import org.openscience.cdk.qsar.result.IntegerResult;
import org.openscience.cdk.silent.SilentChemObjectBuilder;

/**
 * Wraps a {@link IMolecularDescriptor} and provides a method to calculate the descriptor for a given molecule.
 */
public class WrappedMolecularDescriptor {

  private static Logger LOG = Logger.getLogger(WrappedMolecularDescriptor.class.getSimpleName() );

  private final IMolecularDescriptor descriptor;
  private final Function<IDescriptorResult, DoubleStream> resultToStream;
  private final int numDescriptors;

  public WrappedMolecularDescriptor(IMolecularDescriptor descriptor) {
    this.descriptor = Objects.requireNonNull(descriptor);
    descriptor.initialise(new SilentChemObjectBuilder());
    numDescriptors = descriptor.getDescriptorResultType().length();
    resultToStream = switch (descriptor.getDescriptorResultType().getClass().getSimpleName()) {
      case "BooleanResult", "BooleanResultType" ->
        r -> DoubleStream.of(((BooleanResult) r).booleanValue() ? 1.0 : 0.0);
      case "IntegerResult", "IntegerResultType" ->
        r -> DoubleStream.of(((IntegerResult) r).intValue());
      case "DoubleResult", "DoubleResultType" ->
        r -> DoubleStream.of(((DoubleResult) r).doubleValue());
      case "IntegerArrayResult", "IntegerArrayResultType" ->
        r -> getAll(i -> ((IntegerArrayResult) r).get(i));
      case "DoubleArrayResult", "DoubleArrayResultType" ->
        r -> getAll(i -> ((DoubleArrayResult) r).get(i));
      default -> throw new IllegalStateException("Don't know how to handle the " + descriptor.getDescriptorResultType().getClass().getSimpleName() + " result type for " + this);
    };
  }

  private DoubleStream getAll(IntToDoubleFunction f) {
    return IntStream.range(0, numDescriptors).mapToDouble(i -> {
      try {
        return f.applyAsDouble(i);
      } catch (RuntimeException e) {
        LOG.warning("Ignoring exception during get, descriptor replaced with NaN");
        return Double.NaN;
      }
    });
  }

  public DoubleStream calculate(final IAtomContainer mol) {
    IDescriptorResult res = null;
    try {
      final DescriptorValue val = descriptor.calculate(mol.clone());
      if (val != null) res = val.getValue();
    } catch (CloneNotSupportedException | RuntimeException e) {
      LOG.warning("Ignoring exception during clone/calculate/getValue, descriptors replaced with " + numDescriptors + " NaN" + (numDescriptors > 1 ? "(s)" : ""));
    }
    if (res == null) return DoubleStream.generate(() -> Double.NaN).limit(numDescriptors);
    return resultToStream.apply(res);
  }

  public String name() {
    return descriptor.getClass().getSimpleName();
  }

  public String[] descriptors() {
    return descriptor.getDescriptorNames();
  }

  public int numDescriptors() {
    return numDescriptors;  
  }

  @Override
  public String toString() {
    return name() + ": " + String.join(", ", descriptors());
  }
}
