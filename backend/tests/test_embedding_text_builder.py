import pytest
from app.services.embeddings.text_builder import build_embedding_text

def test_build_embedding_text_full():
    book = {
        "title": "Network Security Essentials",
        "subtitle": "Applications and Standards",
        "authors": ["William Stallings"],
        "subjects": ["Computer Science", "Cybersecurity", "Networking"],
        "categories": ["Security", "Networks"],
        "description": "A comprehensive guide to network security."
    }
    
    text = build_embedding_text(book)
    
    assert "Title: Network Security Essentials - Applications and Standards" in text
    assert "Authors: William Stallings" in text
    assert "Subjects: Computer Science, Cybersecurity, Networking" in text
    assert "Categories: Security, Networks" in text
    assert "Description: A comprehensive guide to network security." in text

def test_build_embedding_text_partial():
    book = {
        "title": "Minimal Book",
        "description": "Just a title and description."
    }
    
    text = build_embedding_text(book)
    
    assert "Title: Minimal Book" in text
    assert "Description: Just a title and description." in text
    assert "Authors:" not in text
    assert "Subjects:" not in text
    assert "Categories:" not in text

def test_build_embedding_text_whitespace_normalization():
    book = {
        "title": "Test Book",
        "description": "This   has \n excessive \t whitespace."
    }
    
    text = build_embedding_text(book)
    assert "Description: This has excessive whitespace." in text

def test_build_embedding_text_truncation():
    long_desc = "A" * 2000
    book = {
        "title": "Long Book",
        "description": long_desc
    }
    
    text = build_embedding_text(book)
    assert "Description:" in text
    assert "..." in text
    assert len(text) < 1600 # 1497 + "..." + "Description: " + "Title: Long Book" + newlines
