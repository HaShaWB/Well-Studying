import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:pdfrx/pdfrx.dart';

class scan_page extends StatefulWidget {
  final String format_name;

  const scan_page({super.key, required this.format_name});

  @override
  State<scan_page> createState() => _scan_pageState();
}

class _scan_pageState extends State<scan_page> {
  PdfDocument? pdfDocument;

  Future<void> _pickAndShowPdf() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null) {
      String path = result.files.single.path!;
      final doc = await PdfDocument.openFile(path);
      setState(() {
        pdfDocument = doc;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.format_name),
        actions: [
          IconButton(
            icon: Icon(Icons.file_open),
            onPressed: _pickAndShowPdf, // 파일 선택 기능을 연결합니다.
          ),
        ],
      ),
      body: Column(
        children: [
          pdfDocument == null
              ? const Center(child: Text('PDF 파일을 선택하세요.'))
              : PdfViewer(document: pdfDocument!),
        ],
      ), // PDF 파일을 표시합니다.
    );
  }
}
