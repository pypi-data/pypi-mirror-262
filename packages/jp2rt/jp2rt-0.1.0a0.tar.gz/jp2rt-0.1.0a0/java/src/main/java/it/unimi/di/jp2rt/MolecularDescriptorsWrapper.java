package it.unimi.di.jp2rt;

import java.util.Iterator;
import java.util.List;
import java.util.StringJoiner;
import java.util.logging.Logger;
import java.util.stream.DoubleStream;
import java.util.stream.Stream;

import org.openscience.cdk.exception.CDKException;
import org.openscience.cdk.exception.InvalidSmilesException;
import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.qsar.descriptors.molecular.ALOGPDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.APolDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AcidicGroupCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AminoAcidCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AromaticAtomsCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AromaticBondsCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AtomCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.AutocorrelationDescriptorCharge;
import org.openscience.cdk.qsar.descriptors.molecular.AutocorrelationDescriptorMass;
import org.openscience.cdk.qsar.descriptors.molecular.AutocorrelationDescriptorPolarizability;
import org.openscience.cdk.qsar.descriptors.molecular.BCUTDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.BPolDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.BasicGroupCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.BondCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.CarbonTypesDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.ChiChainDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.ChiClusterDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.ChiPathClusterDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.ChiPathDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.EccentricConnectivityIndexDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.FMFDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.FractionalCSP3Descriptor;
import org.openscience.cdk.qsar.descriptors.molecular.FractionalPSADescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.FragmentComplexityDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.HBondAcceptorCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.HBondDonorCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.HybridizationRatioDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.JPlogPDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.KappaShapeIndicesDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.KierHallSmartsDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.LargestChainDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.LargestPiSystemDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.MDEDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.MannholdLogPDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.PetitjeanNumberDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.PetitjeanShapeIndexDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.RotatableBondsCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.RuleOfFiveDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.SmallRingDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.SpiroAtomCountDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.TPSADescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.VAdjMaDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.WeightDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.WeightedPathDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.WienerNumbersDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.XLogPDescriptor;
import org.openscience.cdk.qsar.descriptors.molecular.ZagrebIndexDescriptor;
import org.openscience.cdk.silent.SilentChemObjectBuilder;
import org.openscience.cdk.smiles.SmilesParser;

public class MolecularDescriptorsWrapper implements Iterable<WrappedMolecularDescriptor> {

  private static Logger LOG = Logger.getLogger(WrappedMolecularDescriptor.class.getSimpleName());

  private final SmilesParser smilesParser = new SmilesParser(new SilentChemObjectBuilder());
  private final List<WrappedMolecularDescriptor> calculators;
  private final int numCols;

  public MolecularDescriptorsWrapper() {
    try {
      calculators = Stream.of(
          new AcidicGroupCountDescriptor(),
          new ALOGPDescriptor(),
          new AminoAcidCountDescriptor(),
          new APolDescriptor(),
          new AromaticAtomsCountDescriptor(),
          new AromaticBondsCountDescriptor(),
          new AtomCountDescriptor(),
          new AutocorrelationDescriptorCharge(),
          new AutocorrelationDescriptorMass(),
          new AutocorrelationDescriptorPolarizability(),
          new BasicGroupCountDescriptor(),
          new BCUTDescriptor(),
          new BondCountDescriptor(),
          new BPolDescriptor(),
          new CarbonTypesDescriptor(),
          new ChiChainDescriptor(),
          new ChiClusterDescriptor(),
          new ChiPathClusterDescriptor(),
          new ChiPathDescriptor(),
          new EccentricConnectivityIndexDescriptor(),
          new FMFDescriptor(),
          new FractionalCSP3Descriptor(),
          new FractionalPSADescriptor(),
          new FragmentComplexityDescriptor(),
          new HBondAcceptorCountDescriptor(),
          new HBondDonorCountDescriptor(),
          new HybridizationRatioDescriptor(),
          new JPlogPDescriptor(),
          new KappaShapeIndicesDescriptor(),
          new KierHallSmartsDescriptor(),
          new LargestChainDescriptor(),
          new LargestPiSystemDescriptor(),
          new MannholdLogPDescriptor(),
          new MDEDescriptor(),
          new PetitjeanNumberDescriptor(),
          new PetitjeanShapeIndexDescriptor(),
          new RotatableBondsCountDescriptor(),
          new RuleOfFiveDescriptor(),
          new SmallRingDescriptor(),
          new SpiroAtomCountDescriptor(),
          new TPSADescriptor(),
          new VAdjMaDescriptor(),
          new WeightDescriptor(),
          new WeightedPathDescriptor(),
          new WienerNumbersDescriptor(),
          new XLogPDescriptor(),
          new ZagrebIndexDescriptor()).map(WrappedMolecularDescriptor::new).toList();
    } catch (CDKException e) {
      throw new IllegalStateException("Problems instantiating descriptors", e);
    }
    numCols = calculators.stream().mapToInt(WrappedMolecularDescriptor::numDescriptors).sum();
  }

  public TSVLine calculate(final TSVLine line) {
    try {
      final IAtomContainer mol = smilesParser.parseSmiles(line.smiles());
      return line.descriptors(calculators.stream().flatMapToDouble(c -> c.calculate(mol)));
    } catch (InvalidSmilesException e) {
      LOG.warning("Could not parse the SMILES " + line.smiles() + " on line " + line + ", descriptors replaced with "
          + numCols + " NaN" + (numCols > 1 ? "(s)" : ""));
      return line.descriptors(DoubleStream.generate(() -> Double.NaN).limit(numCols));
    }
  }

  @Override
  public String toString() {
    int n = 1;
    StringJoiner sj = new StringJoiner("\n", "", "");
    for (WrappedMolecularDescriptor wd : calculators) {
      sj.add(wd.name());
      for (String s : wd.descriptors())
        sj.add("\t" + (n++) + ": " + s);
    }
    return sj.toString();
  }

  @Override
  public Iterator<WrappedMolecularDescriptor> iterator() {
    return calculators.iterator();
  }

}