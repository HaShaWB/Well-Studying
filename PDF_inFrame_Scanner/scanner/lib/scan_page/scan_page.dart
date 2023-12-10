// ignore_for_file: camel_case_types, non_constant_identifier_names

import 'package:flutter/material.dart';
import 'package:pdf_render/pdf_render.dart';
import 'package:pdf_render/pdf_render_widgets.dart';
import 'package:file_picker/file_picker.dart';

class scan_page extends StatefulWidget {
  final String format_name;

  const scan_page({super.key, required this.format_name});

  @override
  State<scan_page> createState() => _scan_pageState();
}

class _scan_pageState extends State<scan_page> {
  String? _pdfPath;
  int _currentPage = 1;
  int _totalPages = 0;
  Future<PdfDocument>? _pdfDocument;

  Future<void> _pickPdfFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null) {
      setState(() {
        _pdfPath = result.files.single.path;
        _pdfDocument = PdfDocument.openFile(_pdfPath!);
        _currentPage = 1; // 새 PDF를 선택할 때마다 페이지를 1로 초기화
      });
    }
  }

  void _gotoPage(int pageNumber) {
    setState(() {
      _currentPage = pageNumber.clamp(1, _totalPages);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.format_name),
        actions: [
          IconButton(
            icon: Icon(Icons.file_open),
            onPressed: _pickPdfFile,
          ),
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () {
              // '+' 버튼 기능 추가
            },
          ),
          IconButton(
            icon: Icon(Icons.remove),
            onPressed: () {
              // '-' 버튼 기능 추가
            },
          ),
          IconButton(
            icon: Icon(Icons.save),
            onPressed: () {
              // '저장' 버튼 기능 추가
            },
          ),
        ],
      ),
      body: _pdfDocument == null
          ? Center(child: Text('PDF 파일을 선택하세요.'))
          : FutureBuilder<PdfDocument>(
              future: _pdfDocument,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  _totalPages = snapshot.data!.pageCount;
                  return PdfDocumentLoader(
                    doc: snapshot.data!,
                    pageNumber: _currentPage,
                    pageBuilder: (context, textureBuilder, pageSize) {
                      return textureBuilder();
                    },
                  );
                } else if (snapshot.hasError) {
                  return Center(child: Text("Error loading document"));
                } else {
                  return Center(child: CircularProgressIndicator());
                }
              },
            ),
      bottomNavigationBar: _pdfDocument == null
          ? SizedBox()
          : BottomAppBar(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  IconButton(
                    icon: Icon(Icons.chevron_left),
                    onPressed: _currentPage > 1
                        ? () => _gotoPage(_currentPage - 1)
                        : null,
                  ),
                  Text('Page $_currentPage of $_totalPages'),
                  IconButton(
                    icon: Icon(Icons.chevron_right),
                    onPressed: _currentPage < _totalPages
                        ? () => _gotoPage(_currentPage + 1)
                        : null,
                  ),
                ],
              ),
            ),
    );
  }
}
