
import os
import PyPDF2

def process_document(doc_name, copies_count, correction_map=None):
    base_dir = r"c:\Users\afd\Desktop\exam-ASD-S1-25-26"
    source_pdf_path = os.path.join(base_dir, f"{doc_name}.pdf")
    
    code_split_dir = os.path.join(base_dir, "extracted_code", "pdf", "split")
    corr_split_dir = os.path.join(base_dir, "extracted_code", "corrections", "split")
    
    output_dir = os.path.join(base_dir, "final_output", doc_name)
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(source_pdf_path):
        print(f"Skipping {doc_name}: Source not found")
        return

    # Keep source file open during the entire processing
    try:
        with open(source_pdf_path, 'rb') as f_source:
            reader_source = PyPDF2.PdfReader(f_source)
            num_source_pages = len(reader_source.pages)

            print(f"Processing {doc_name}: Source Pages={num_source_pages}, Expected Copies={copies_count}")

            copies_list = []
            if doc_name == "doc20260115222526":
                copies_list = list(range(1, 23)) + [24, 25] 
            else:
                start_copy = 1
                if doc_name == "doc20260115223319": start_copy = 1
                elif doc_name == "doc20260115223647": start_copy = 13
                elif doc_name == "doc20260115223525": start_copy = 8
                
                copies_list = list(range(start_copy, start_copy + copies_count))

            pages_per_copy = 1
            if doc_name in ["doc20260115223319", "doc20260115223525", "doc20260115223647"]:
                pages_per_copy = 2
                print(f"  Detected 2 source pages per copy for this document.")
            
            idx_source = 0
            
            for copy_num in copies_list:
                merger = PyPDF2.PdfWriter()
                
                # 1. Add Source Page(s)
                if idx_source < num_source_pages:
                    for _ in range(pages_per_copy):
                        if idx_source < num_source_pages:
                            merger.add_page(reader_source.pages[idx_source])
                            idx_source += 1
                else:
                    print(f"  Warning: No source page for Copy {copy_num}")

                # 2. Add Code PDF
                code_split_name = f"code_{doc_name}_Copy_{copy_num}.pdf"
                code_split_path = os.path.join(code_split_dir, code_split_name)
                
                f_code = None
                if os.path.exists(code_split_path):
                    try:
                        f_code = open(code_split_path, 'rb')
                        reader_code = PyPDF2.PdfReader(f_code)
                        for p in reader_code.pages:
                            merger.add_page(p)
                    except Exception as e:
                        print(f"  Error adding code PDF {code_split_name}: {e}")
                else:
                    print(f"  Warning: Code split file missing: {code_split_name}")

                # 3. Add Correction PDF
                corr_split_name = f"Corr_{doc_name}_Copy_{copy_num}.pdf"
                corr_split_path = os.path.join(corr_split_dir, corr_split_name)
                
                f_corr = None
                if os.path.exists(corr_split_path):
                    try:
                        f_corr = open(corr_split_path, 'rb')
                        reader_corr = PyPDF2.PdfReader(f_corr)
                        for p in reader_corr.pages:
                            merger.add_page(p)
                    except Exception as e:
                        print(f"  Error adding corr PDF {corr_split_name}: {e}")
                else:
                     print(f"  Warning: Corr split file missing: {corr_split_name}")
                
                # Save Final PDF
                out_name = f"Etudiant_Copie_{copy_num}.pdf"
                out_path = os.path.join(output_dir, out_name)
                
                try:
                    with open(out_path, 'wb') as f_out:
                        merger.write(f_out)
                except Exception as e:
                    print(f"  Failed to save {out_path}: {e}")
                finally:
                    # Close sub-files
                    if f_code: f_code.close()
                    if f_corr: f_corr.close()
                    
    except Exception as e:
        print(f"Error processing {doc_name}: {e}")

# Main execution
docs = [
    ("doc20260115201344", 24),
    ("doc20260115220910", 18),
    ("doc20260115221134", 22),
    ("doc20260115222526", 24), # Copy 23 missing handled inside
    ("doc20260115223319", 7),
    ("doc20260115223647", 4),
    ("doc20260115223525", 5),
    ("doc20260115221404", 24),
    ("doc20260115221630", 28),
    ("doc20260115222057", 23),
    ("doc20260115222309", 26)
]

for name, count in docs:
    process_document(name, count)
