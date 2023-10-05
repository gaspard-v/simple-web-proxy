import { encode, decode } from "@abcnews/base-36-text";

export function test() {
    const string = "I am a test &é*µù$^^";
    const foo = encode(string);
    console.log(foo);
    const bar = decode(foo);
    console.log(bar);
}
