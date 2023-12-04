import 'dart:io';
import 'package:path_provider/path_provider.dart';

class file_tackling {
  late final String _path;

  FileTackling._create(this._path);

  static Future<FileTackling> create() async {
    final directory = await getApplicationDocumentsDirectory();
    return FileTackling._create(directory.path);
  }
  
}
