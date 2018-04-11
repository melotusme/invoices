##!/usr/local/opt/coreutils/libexec/gnubin/env ruby
require 'mail'
require 'pry'
require 'nokogiri'
require 'rest-client'
require 'digest/sha1'
require 'fileutils'

smtp = { address: 'smtp.163.com', port: 25,user_name: 'xxx@163.com', password: 'xxx', enable_ssl: false}
pop3 = { address: 'pop.163.com', port: 110,user_name: 'xxx@163.com', password: 'xxx', enable_ssl: false}

Mail.defaults do
  delivery_method :smtp, smtp
  retriever_method :pop3, pop3
end

mails = Mail.last count: 8,order: :desc
mails.select! {|m| /发票/ =~ m.subject}
mails.each do|m|
  handle_jd(m)
end

def handle_jd(m)
  doc = Nokogiri::HTML m.body.to_s
  n = doc.css("tr td a").select{|n| n.text == "电子普通发票下载"}
  url = n.first['href']
  response = RestClient.get url
  body =response.body
  file_name = Digest::SHA1.hexdigest body
  dst_path = "/Users/wrong/namespaces/ruby/#{file_name}.pdf"
  File.open(dst_path, "w"){|f| f.write response.body}
end
