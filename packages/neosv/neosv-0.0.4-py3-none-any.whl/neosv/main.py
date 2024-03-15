import os
from .args import create_arg_parser
from .input import vcf_load, bedpe_load, hla_load, ensembl_load, get_window_range
from .sv_utils import sv_pattern_infer_vcf, sv_pattern_infer_bedpe, remove_duplicate
from .annotation_utils import sv_to_sveffect
from .fusion_utils import sv_to_svfusion
from .sequence_utils import set_nt_seq, set_aa_seq, generate_neoepitopes
from .netMHC import netmhc_pep_prep, netmhc_run, netmhc_reload, netmhc_filter
from .output import write_annot, write_fusion


def main():
    # generate the args
    args = create_arg_parser()
    # load a pyensembl Genome class
    ensembl = ensembl_load(args.release, args.gtffile, args.cdnafile, args.cachedir)

    if args.svfile.endswith('.vcf'):
        # load vcf file and transform SVs into VariantCallingFormat class
        sv_vcfs = vcf_load(args.svfile)
        # transform SV from VariantCallingFormat class to StructuralVariant class
        svs = [sv_pattern_infer_vcf(sv_vcf) for sv_vcf in sv_vcfs]
    elif args.svfile.endswith('.bedpe'):
        # load vcf file and transform SVs into BEDPE class
        sv_beds = bedpe_load(args.svfile)
        # transform SV from BEDPE class to StructuralVariant class
        svs = [sv_pattern_infer_bedpe(sv_bed) for sv_bed in sv_beds]
    else:
        sys.exit('The input file must end with .vcf or .bedpe. Other format is not allowed.')
    # remove duplicated SVs
    svs = remove_duplicate(svs)

    # annotate SVs and write to file_anno
    sv_effects = [sv_to_sveffect(sv, ensembl, args.complete) for sv in svs]
    sv_effects_flat = [sv_effect_unit for sv_effect in sv_effects for sv_effect_unit in sv_effect]
    file_anno = os.path.join(args.outdir, args.prefix + '.anno.txt')
    write_annot(file_anno, sv_effects_flat)

    if not args.anno:
        # load the hla file and join the alleles by ,
        hla_alleles = hla_load(args.hlafile)
        # specify the lengths of neoepitopes you want to predict
        window_range = get_window_range(args.window)
        # transform StructuralVariant class to SVFusion class
        sv_fusions = [sv_to_svfusion(sv, ensembl) for sv in svs]
        # remove those empty SVFusions
        sv_fusions = [sv_fusion for sv_fusion in sv_fusions if not sv_fusion.is_empty()]

        # predict neoepitopes for each SVFusion
        for sv_fusion in sv_fusions:
            sv_fusion.nt_sequence = set_nt_seq(sv_fusion)
            sv_fusion.aa_sequence = set_aa_seq(sv_fusion)
            sv_fusion.neoepitopes = generate_neoepitopes(sv_fusion, window_range)

        # predict binding affinity using netMHC
        file_netmhc_in = os.path.join(args.outdir, args.prefix + '.net.in.txt')
        file_netmhc_out = os.path.join(args.outdir, args.prefix + '.net.out.txt')
        if sv_fusions:
            netmhc_pep_prep(file_netmhc_in, sv_fusions)
            netmhc_run(args.netmhc, file_netmhc_in, hla_alleles, file_netmhc_out)
        else:
            open(file_netmhc_in, 'w').close()
            open(file_netmhc_out, 'w').close()

        # reload and filter the neoepitopes based on netMHC result
        dict_epitope = netmhc_reload(file_netmhc_out)
        dict_epitope = netmhc_filter(dict_epitope, args.aff_cutoff, args.ba_rank_cutoff, args.el_rank_cutoff)

        # generate the final outfile
        file_fusion = os.path.join(args.outdir, args.prefix + '.neoantigen.txt')
        write_fusion(file_fusion, sv_fusions, dict_epitope)


if __name__ == '__main__':
    main()
