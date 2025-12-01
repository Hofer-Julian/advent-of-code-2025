const std = @import("std");

pub fn main() !void {
    var args = std.process.args();
    _ = args.skip();
    const input_file = args.next() orelse return error.MissingArgument;

    const file = try std.fs.cwd().openFile(input_file, .{});
    defer file.close();

    const input = try file.readToEndAlloc(std.heap.page_allocator, std.math.maxInt(usize));
    defer std.heap.page_allocator.free(input);

    std.debug.print("Input: {s}\n", .{input});
}
