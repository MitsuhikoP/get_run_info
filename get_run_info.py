#!/usr/bin/env python3
# copyright (c) 2019 Mitsuhiko Sato. All Rights Reserved.
# Mitsuhiko Sato ( E-mail: mitsuhikoevolution@gmail.com )
#coding:UTF-8

def main():
    from argparse import ArgumentParser,FileType
    import os
    parser=ArgumentParser(description="",usage="You can see help: python3 get_run_info.py -h", epilog="")
    parser.add_argument("dirs", nargs="+", type=str, metavar="dir", help="MiSeq 
directory (more than 1 file(s) )")
    parser.add_argument("--mode", type=str, choices=["list", "add", "show"], met
avar="list|add|show", default="show", help="mode type. list, add, or show (defau
lt=show)")
    parser.add_argument("-O", type=str, metavar="str", help="output file name" )
    
    parser.add_argument("-o", type=str, metavar="str",default="unknown",help="op
erator name (default = unknown)")
    parser.add_argument("-l", type=str, metavar="str",default="unknown",help="Li
brary prep (default = unknown)")
    parser.add_argument("-s", type=str, metavar="str",default="unknown",help="sa
mple information (default = unknown)" )
    parser.add_argument("-c", type=str, metavar="str",default="NO_COMMENT",help=
"comment (default = NO_COMMENT)" )
    
    args = parser.parse_args()
    outs=""
    for file in args.dirs:
        if not os.path.exists(file+"/SampleSheet.csv"):
            continue
        if not os.path.exists(file+"/GenerateFASTQRunStatistics.xml"):
            continue
        
        out={"dir":file.split("/")[-1]}
        print(file)
        fhr=open(file+"/SampleSheet.csv")
        for line in fhr:
            lines=line.split(",")
            if lines[0] == "Experiment Name":
                out["Exp"]=lines[1]
            elif lines[0] == "Date":
                out["Date"]=lines[1]
            elif lines[0] == "Chemistry":
                out["Chem"]=lines[1]
            elif lines[0] == "[Reads]":
                while True:
                    lines=fhr.readline().split(",")
                    if lines[0] == "":
                        break
                    if "Reads" in out:
                        out["Reads"] += "/"+lines[0]
                    else:
                        out["Reads"] = lines[0]
                        
            elif lines[0] == "[Data]":
                count=0
                smpl_name=""
                fhr.readline()
                for smpl in fhr:
                    smpls=smpl.split(",")
                    if smpls[1] != "PhiX":
                        count+=1
                        smpl_name+=smpls[1]+","
                out["num_samples"]=count
                out["sample_name"]=smpl_name                    
        fhr.close()

        fhr=open(file+"/GenerateFASTQRunStatistics.xml")
        for line in fhr:
            if line.startswith("    <NumberOfClustersPF>"):
                line=line.lstrip("    <NumberOfClustersPF>")
                line=line.rstrip("</NumberOfClustersPF>\n")
                out["ClusterPF"]=line
            if line.startswith("    <NumberOfClustersRaw>"):
                line=line.lstrip("    <NumberOfClustersRaw>")
                line=line.rstrip("</NumberOfClustersRaw>\n")
                out["ClusterRaw"]=line                
            elif line == "  </RunStats>":
                break
  
        if args.mode == "show":
            for o in out:
                print(o,out[o])
            print("%PF "+str(float(out["ClusterPF"])/float(out["ClusterRaw"])*100))
        else:
            if not "Date" in out:
                out["Date"] = "NA"
            if not "Exp" in out:
                out["Exp"] = "NA"
            if not "Chem" in out:
                out["Chem"] = "NA"
            if not "Reads" in out:
                out["Reads"] = "NA"
            if not "num_samples" in out:
                out["num_samples"] = 0
            if not "sample_name" in out:
                out["sample_name"] = "NA"
            
                
        outs+=out["dir"]+"\t"+out["Date"]+"\t"+args.o+"\t"+args.l+"\t"+args.s+"\t"+args.c+"\t"+out["Exp"]+"\t"+out["Chem"]+"\t"+out["Reads"]+"\t"+str(out["num_samples"])+"\t"+str(out["ClusterPF"])+"\t"+out["ClusterRaw"]+"\t"+str(float(out["ClusterPF"])/float(out["ClusterRaw"])*100)+"\t"+out["sample_name"]+"\n"

    if args.mode == "add":
        
        fhw=open(args.O,"a")
        fhw.write(outs)
        fhw.close()
    elif args.mode == "list":
        fhw=open(args.O,"w")
        label="Name\tDate\tOPERATOR\tLibrary_Prep\tSample_information\tcomment\tExperiment Name\tChemistry\tReads\tnum samples\tNumberOfClusterPF\tNumberOfClusterRaw\t%PF\tsample names\n"
        fhw.write(label)
        fhw.write(outs)
        fhw.close()
            
if __name__ == '__main__': main()

